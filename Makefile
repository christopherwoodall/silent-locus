# Silent Locus — local ELK stack.
# Self-documenting: every target carries a ## description; `make` (or
# `make help`) prints them, grouped by the ##@ section headers below.

ES_URL     ?= http://localhost:9200
KIBANA_URL ?= http://localhost:5601
ES_USER    ?= elastic
ES_PASS    ?= changeme
PY         ?= python3
COMPOSE    ?= docker compose
DASHBOARD_FILE ?= $(lastword $(sort $(wildcard kibana-exports/all-dashboards-*.ndjson)))

# Ingest scripts (push_to_local_es.py and the patched es_ingest_*.py)
# read these from the environment.
export ES_URL ES_USER ES_PASS

.DEFAULT_GOAL := help

.PHONY: help doctor up down restart ps logs logs-es logs-kibana wait status kibana \
        ingest ingest-corpus ingest-swarmtraces verify-ingest ingest-dashboards \
        dry-run validate validate-collections verify-checksums test clean reset

##@ Stack

help: ## Show this help
	@awk 'BEGIN {FS = ":.*## "; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*## / {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2} /^##@/ {printf "\n%s\n", substr($$0, 5)}' $(MAKEFILE_LIST)

doctor: ## Check local prerequisites (docker, compose, python, curl)
	@command -v docker >/dev/null 2>&1 && echo "docker:  $$(docker version --format '{{.Server.Version}}' 2>/dev/null || echo 'installed, daemon not reachable')" || echo "docker:  MISSING"
	@$(COMPOSE) version >/dev/null 2>&1 && echo "compose: OK" || echo "compose: MISSING"
	@command -v $(PY) >/dev/null 2>&1 && echo "python:  $$($(PY) --version 2>&1)" || echo "python:  MISSING"
	@command -v curl >/dev/null 2>&1 && echo "curl:    OK" || echo "curl:    MISSING"
	@echo "note:    ES needs vm.max_map_count >= 262144; Docker Desktop's VM already sets this"

up: ## Start Elasticsearch + Kibana in the background
	@mkdir -p elk/data
	$(COMPOSE) up -d

down: ## Stop the stack (./elk/data is kept)
	$(COMPOSE) down

restart: ## Restart the stack
	$(COMPOSE) restart

ps: ## Show container status
	$(COMPOSE) ps

logs: ## Tail logs from all services
	$(COMPOSE) logs -f

logs-es: ## Tail Elasticsearch logs
	$(COMPOSE) logs -f elasticsearch

logs-kibana: ## Tail Kibana logs
	$(COMPOSE) logs -f kibana

wait: ## Wait until Elasticsearch answers and cluster health is not red
	@echo "waiting for $(ES_URL) ..."; \
	for i in $$(seq 1 90); do \
	  s=$$(curl -s -u "$(ES_USER):$(ES_PASS)" "$(ES_URL)/_cluster/health" 2>/dev/null | grep -o '"status":"[a-z]*"' | head -1 | cut -d'"' -f4); \
	  if [ "$$s" = "green" ] || [ "$$s" = "yellow" ]; then echo "cluster status: $$s"; exit 0; fi; \
	  sleep 2; \
	done; \
	echo "timed out waiting for Elasticsearch (try: make logs-es)"; exit 1

status: ## List indices with doc counts
	@curl -s -u "$(ES_USER):$(ES_PASS)" "$(ES_URL)/_cat/indices?v&s=index"

kibana: ## Print local URLs and login name
	@echo "Elasticsearch: $(ES_URL)  (login: $(ES_USER))"
	@echo "Kibana:        $(KIBANA_URL)  (login: $(ES_USER); password: ES_PASS)"

##@ Ingest

ingest: ## Start stack, load both datasets, and verify every index (dashboards optional)
	$(MAKE) up
	$(MAKE) wait
	$(MAKE) ingest-corpus
	$(MAKE) ingest-swarmtraces
	$(MAKE) verify-ingest

ingest-corpus: wait ## Load all registered events.jsonl and rollup.jsonl files
	$(PY) scripts/push_to_local_es.py --all

ingest-swarmtraces: wait ## Load data/raw/redacted.jsonl.gz (189,579 records) into the swarmtraces index
	$(PY) scripts/es_ingest_swarmtraces.py --check-source
	$(PY) scripts/es_ingest_swarmtraces.py --create
	$(PY) scripts/es_ingest_swarmtraces.py --load
	$(PY) scripts/es_ingest_swarmtraces.py --verify

verify-ingest: wait ## Compare all local index counts with distinct staged document IDs
	$(PY) scripts/push_to_local_es.py --all --verify
	$(PY) scripts/es_ingest_swarmtraces.py --verify

ingest-dashboards: ## Optionally import DASHBOARD_FILE (latest export by name) into Kibana
	@f="$(DASHBOARD_FILE)"; \
	[ -f "$$f" ] || { echo "dashboard export not found: $$f"; exit 1; }; \
	echo "waiting for Kibana at $(KIBANA_URL) ..."; \
	for i in $$(seq 1 90); do \
	  code=$$(curl -s -o /dev/null -w '%{http_code}' -u "$(ES_USER):$(ES_PASS)" "$(KIBANA_URL)/api/status" 2>/dev/null); \
	  [ "$$code" = "200" ] && break; sleep 2; \
	done; \
	[ "$$code" = "200" ] || { echo "Kibana not ready (last HTTP $$code)"; exit 1; }; \
	echo "importing $$f"; \
	response=$$(curl --fail-with-body -sS -u "$(ES_USER):$(ES_PASS)" -X POST \
	  "$(KIBANA_URL)/api/saved_objects/_import?overwrite=true" \
	  -H "kbn-xsrf: true" --form "file=@$$f") \
	  || { echo "dashboard import HTTP request FAILED (check export compatibility with local Kibana)"; exit 1; }; \
	printf '%s' "$$response" | $(PY) -c \
	  'import json, sys; r = json.load(sys.stdin); print("dashboards imported:", r.get("successCount", "?")) if r.get("success") is True else print("dashboard import FAILED"); sys.exit(0 if r.get("success") is True else 1)'

dry-run: ## Preview everything (corpus plan, dataset counts); writes nothing
	$(PY) scripts/push_to_local_es.py --dry-run
	$(PY) scripts/es_ingest_swarmtraces.py --dry-run

##@ Validation

validate: ## Record-schema + collection validation; exits non-zero on violations
	$(PY) scripts/validate_schema.py
	$(PY) scripts/validate_collections.py

validate-collections: ## Collection naming/registration/right-directory checks only
	$(PY) scripts/validate_collections.py

verify-checksums: ## Audit all collection manifests; fail on missing or changed bytes
	$(PY) -B scripts/verify_checksums.py

test: ## Run offline regression tests without contacting Elasticsearch
	$(PY) -B -m unittest discover -s tests -p 'test_*.py'

##@ Maintenance

clean: ## Delete ALL data indices in the local cluster (containers and ./elk/data stay up)
	@printf "This deletes every non-system index on %s. Type 'clean' to confirm: " "$(ES_URL)"; \
	read a; [ "$$a" = "clean" ] || { echo "aborted"; exit 1; }; \
	for idx in $$(curl -s -u "$(ES_USER):$(ES_PASS)" "$(ES_URL)/_cat/indices?h=index" | grep -v '^\.'); do \
	  printf "deleting %s ... " "$$idx"; \
	  curl -s -u "$(ES_USER):$(ES_PASS)" -X DELETE "$(ES_URL)/$$idx" | grep -q '"acknowledged":true' \
	    && echo "ok" || echo "FAILED"; \
	done

reset: ## Stop the stack AND wipe ./elk/data (full wipe)
	@printf "This stops the stack and wipes ./elk/data. Type 'reset' to confirm: "; \
	read a; [ "$$a" = "reset" ] || { echo "aborted"; exit 1; }; \
	$(COMPOSE) down; \
	rm -rf ./elk/data && mkdir -p ./elk/data && echo "elk/data wiped"

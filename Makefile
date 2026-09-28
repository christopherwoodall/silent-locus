# Silent Locus — local ELK stack.
# Self-documenting: every target carries a ## description; `make` (or
# `make help`) prints them, grouped by the ##@ section headers below.

ES_URL     ?= http://localhost:9200
KIBANA_URL ?= http://localhost:5601
ES_USER    ?= elastic
ES_PASS    ?= changeme
PY         ?= python3
COMPOSE    ?= docker compose

# Ingest scripts (push_to_local_es.py and the patched es_ingest_*.py)
# read these from the environment.
export ES_URL ES_USER ES_PASS

.DEFAULT_GOAL := help

.PHONY: help doctor up down restart ps logs logs-es logs-kibana wait status kibana \
        ingest ingest-snapshot ingest-corpus ingest-swarmtraces ingest-dashboards \
        dry-run clean reset

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
	$(COMPOSE) up -d

down: ## Stop the stack (data volume is kept)
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

kibana: ## Print URLs and credentials
	@echo "Elasticsearch: $(ES_URL)  ($(ES_USER) / $(ES_PASS))"
	@echo "Kibana:        $(KIBANA_URL)  ($(ES_USER) / $(ES_PASS))"

##@ Ingest

ingest: wait ## Full load: snapshot -> corpus -> swarmtraces -> dashboards
	$(MAKE) ingest-snapshot
	$(MAKE) ingest-corpus
	$(MAKE) ingest-swarmtraces
	$(MAKE) ingest-dashboards

ingest-snapshot: wait ## Restore the elastic-exports/*.jsonl.gz cloud snapshot (sha256-verified, original _ids)
	$(PY) scripts/restore_elastic_exports.py

ingest-corpus: wait ## Load the local corpus via scripts/local_es_manifest.json (staged + via_script)
	$(PY) scripts/push_to_local_es.py --all

ingest-swarmtraces: wait ## Load data/raw/redacted.jsonl.gz (189,579 records) into the swarmtraces index
	$(PY) scripts/es_ingest_swarmtraces.py --create
	$(PY) scripts/es_ingest_swarmtraces.py --load
	$(PY) scripts/es_ingest_swarmtraces.py --verify

ingest-dashboards: ## Import the latest kibana-exports/all-dashboards-*.ndjson into Kibana
	@f=$$(ls -t kibana-exports/all-dashboards-*.ndjson 2>/dev/null | head -1); \
	[ -n "$$f" ] || { echo "no dashboard export found in kibana-exports/"; exit 1; }; \
	echo "waiting for Kibana at $(KIBANA_URL) ..."; \
	for i in $$(seq 1 90); do \
	  code=$$(curl -s -o /dev/null -w '%{http_code}' -u "$(ES_USER):$(ES_PASS)" "$(KIBANA_URL)/api/status" 2>/dev/null); \
	  [ "$$code" = "200" ] && break; sleep 2; \
	done; \
	[ "$$code" = "200" ] || { echo "Kibana not ready (last HTTP $$code)"; exit 1; }; \
	echo "importing $$f"; \
	curl -s -u "$(ES_USER):$(ES_PASS)" -X POST \
	  "$(KIBANA_URL)/api/saved_objects/_import?overwrite=true" \
	  -H "kbn-xsrf: true" --form "file=@$$f" | tee /dev/stderr | grep -q '"success":true' \
	  && echo "dashboards imported" || { echo "dashboard import FAILED"; exit 1; }

dry-run: ## Preview everything (snapshot verify, corpus plan, dataset counts); writes nothing
	$(PY) scripts/restore_elastic_exports.py --dry-run
	$(PY) scripts/push_to_local_es.py --dry-run
	$(PY) scripts/es_ingest_swarmtraces.py --dry-run

##@ Maintenance

clean: ## Delete ALL data indices in the local cluster (containers and volume stay up)
	@printf "This deletes every non-system index on %s. Type 'clean' to confirm: " "$(ES_URL)"; \
	read a; [ "$$a" = "clean" ] || { echo "aborted"; exit 1; }; \
	for idx in $$(curl -s -u "$(ES_USER):$(ES_PASS)" "$(ES_URL)/_cat/indices?h=index" | grep -v '^\.'); do \
	  printf "deleting %s ... " "$$idx"; \
	  curl -s -u "$(ES_USER):$(ES_PASS)" -X DELETE "$(ES_URL)/$$idx" | grep -q '"acknowledged":true' \
	    && echo "ok" || echo "FAILED"; \
	done

reset: ## Stop the stack AND delete the esdata volume (full wipe)
	@printf "This stops the stack and wipes the esdata volume. Type 'reset' to confirm: "; \
	read a; [ "$$a" = "reset" ] || { echo "aborted"; exit 1; }; \
	$(COMPOSE) down -v

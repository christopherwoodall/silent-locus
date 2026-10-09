import pytest

from factum_lib.store import State, initialize
from tools.validation_support import git


@pytest.fixture
def repo(tmp_path):
    host = tmp_path / "host with spaces"
    host.mkdir()
    git(host, "init", "-q")
    initialize(host)
    return host


@pytest.fixture
def state(repo):
    return State(repo).load()


@pytest.fixture
def bundle():
    return {
        "bundle": 2, "actor": "agent:synthetic", "idempotency_key": "test/value",
        "tags": {},
        "records": [{
            "ref": "value", "kind": "observable",
            "body": {"type": "domain", "value": "Example.COM"}, "tags": {},
        }],
    }



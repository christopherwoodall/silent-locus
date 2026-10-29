"""
agent_id, token

token: hex(len(task_id) (one byte) + task_info + checksum + random_data)
checksum = sha256(agent_id + task_info + salt)


len(task_info) <= 30
len(checksum) = 32

len(token_bytes) <= 62
"""

import base64
import hashlib
import hmac
from uuid import uuid4

DEFAULT_SALT = "cg-060f0867-f5b2-4572-92d9-3346a250a2d1"
DEFAULT_FLAG_SEED = "sf-1abe0cec-2bea-419a-859a-75b2c13161de"
MAX_TASK_ID_LENGTH = 63
TOKEN_BYTE_LENGTH = 96


def generate_token(
    task_info: str, agent_id: str | None = None, salt: str = DEFAULT_SALT
) -> tuple[str, str]:
    task_info_len = len(task_info)
    if task_info_len > MAX_TASK_ID_LENGTH:
        raise ValueError("task_info is too long")
    if agent_id is None:
        agent_id = uuid4().hex
    checksum = hashlib.sha256(f"{agent_id}{task_info}{salt}".encode()).digest()
    token_bytes = bytes([task_info_len]) + task_info.encode() + checksum
    # Pad with random bytes to reach TOKEN_BYTE_LENGTH
    token_bytes += uuid4().bytes
    token_bytes = token_bytes[:TOKEN_BYTE_LENGTH]
    token = base64.urlsafe_b64encode(token_bytes).decode()
    return agent_id, token


def generate_flag(task_id: str, seed: str = DEFAULT_FLAG_SEED) -> str:
    """Derive a deterministic flag from *seed* and *task_id* via HMAC-SHA256.

    Returns a string like ``flag{<hex>}`` (32 hex chars).
    """
    mac = hmac.new(seed.encode(), task_id.encode(), hashlib.sha256).hexdigest()
    return f"flag{{{mac[:32]}}}"


def verify_token(agent_id: str, token: str, salt: str = DEFAULT_SALT) -> str | None:
    try:
        token_bytes = base64.urlsafe_b64decode(token.encode())
        task_info_len = token_bytes[0]
        task_info = token_bytes[1 : 1 + task_info_len].decode()
        checksum = token_bytes[1 + task_info_len : 1 + task_info_len + 32]
        expected_checksum = hashlib.sha256(
            f"{agent_id}{task_info}{salt}".encode()
        ).digest()
        if checksum == expected_checksum:
            return task_info
    except Exception:
        pass
    return None

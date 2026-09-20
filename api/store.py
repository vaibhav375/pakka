"""Where a scan goes after it is decided.

On AWS this is DynamoDB. Locally it is a JSON file, so the project runs with
nothing installed. The handler does not know or care which one it got.
"""
from __future__ import annotations

import json
import os
import pathlib
import secrets
import time

TABLE = os.environ.get("PAKKA_TABLE")
_LOCAL_PATH = pathlib.Path(os.environ.get("PAKKA_LOCAL_STORE", ".local-store.json"))
TTL_DAYS = 30


def new_id() -> str:
    # short enough to read out in a demo, long enough not to be guessable
    return secrets.token_urlsafe(6)


def _local_load() -> dict:
    if _LOCAL_PATH.exists():
        return json.loads(_LOCAL_PATH.read_text())
    return {}


# Storage is allowed to fail, but it is not allowed to take the answer down
# with it: short timeouts and a single attempt, so a slow or unreachable table
# costs a second and the user still gets their verdict.
_BOTO_CFG = dict(connect_timeout=2, read_timeout=2, retries={"max_attempts": 1})
_table = None


def _get_table():
    global _table
    if _table is None:
        import boto3  # only present in the Lambda runtime
        from botocore.config import Config
        _table = boto3.resource("dynamodb", config=Config(**_BOTO_CFG)).Table(TABLE)
    return _table


def put(scan_id: str, record: dict) -> None:
    record = {**record, "id": scan_id, "created_at": int(time.time())}
    if TABLE:
        _get_table().put_item(
            Item={**record, "expires_at": record["created_at"] + TTL_DAYS * 86400}
        )
        return
    data = _local_load()
    data[scan_id] = record
    _LOCAL_PATH.write_text(json.dumps(data, indent=2))


def get(scan_id: str) -> dict | None:
    if TABLE:
        return _get_table().get_item(Key={"id": scan_id}).get("Item")
    return _local_load().get(scan_id)

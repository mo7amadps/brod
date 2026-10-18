"""تخزين JSON بسيط لبوت البرودكاست المنفصل."""
from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.getenv("BOT_DATA_DIR") or (BASE_DIR / "data"))
DATA_FILE = DATA_DIR / "guilds.json"
_lock = asyncio.Lock()


def _ensure():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("{}", encoding="utf-8")


def _read() -> dict:
    _ensure()
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8") or "{}")
    except Exception:
        return {}


def _write(data: dict) -> None:
    _ensure()
    tmp = DATA_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(DATA_FILE)


def _default_broadcast() -> dict:
    return {
        "tokens": [],
        "message": None,
        "message_id": None,
        "channel_id": None,
        "campaign": None,
        "whitelist_role_id": None,
    }


class Storage:
    @staticmethod
    async def get_guild(guild_id: int) -> dict:
        async with _lock:
            data = _read()
            g = data.get(str(guild_id)) or {}
            if "broadcast" not in g:
                g["broadcast"] = _default_broadcast()
            return g

    @staticmethod
    async def update_guild(guild_id: int, section: str, updates: dict):
        async with _lock:
            data = _read()
            gid = str(guild_id)
            g = data.setdefault(gid, {})
            sec = dict(g.get(section) or {})
            sec.update(updates)
            g[section] = sec
            data[gid] = g
            _write(data)

    @staticmethod
    async def get_broadcast_campaigns(status: str = None) -> list:
        async with _lock:
            data = _read()
            result = []
            for gid, guild_data in data.items():
                campaign = (guild_data.get("broadcast") or {}).get("campaign")
                if not campaign:
                    continue
                if status is not None and campaign.get("status") != status:
                    continue
                result.append((int(gid), dict(campaign)))
            return result

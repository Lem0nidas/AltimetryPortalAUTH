from app.services.rads_sync_tables import get_tables
from datetime import datetime
from pathlib import Path
import json

STATE_FILE = Path("app/utils/update_state.json")


def already_updated():
    if not STATE_FILE.exists():
        return False

    data = json.loads(STATE_FILE.read_text())

    return data.get("date") == datetime.now().date().isoformat()


def mark_updated():
    STATE_FILE.write_text(json.dumps({
        "date": datetime.now().date().isoformat()
    }))


if already_updated():
    print("Already updated today")
    exit()

get_tables()
mark_updated()
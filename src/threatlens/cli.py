import argparse
import json
import logging
from .config import Settings
from .otx import OTXClient
from .storage import Store
from .validators import normalize_indicator

LOG = logging.getLogger("threatlens")

def ingest(pulses: list[dict], store: Store) -> dict:
    counts = {"created": 0, "duplicate": 0, "rejected": 0}
    for pulse in pulses:
        if not isinstance(pulse, dict):
            counts["rejected"] += 1
            continue
        pulse_id = str(pulse.get("id", "unknown"))[:128]
        indicators = pulse.get("indicators", [])
        if not isinstance(indicators, list):
            counts["rejected"] += 1
            continue
        for item in indicators:
            try:
                if not isinstance(item, dict):
                    raise ValueError("Indicator must be an object")
                kind, value = normalize_indicator(item.get("type"), item.get("indicator"))
                created = store.add(kind, value, pulse_id)
                counts["created" if created else "duplicate"] += 1
            except (ValueError, TypeError) as exc:
                counts["rejected"] += 1
                LOG.warning("Rejected indicator from pulse %s: %s", pulse_id, exc)
    return counts

def main():
    parser = argparse.ArgumentParser(description="ThreatLens IOC ingestion (no SIEM writes)")
    parser.add_argument("command", choices=["collect", "sample"])
    parser.add_argument("--file", help="JSON file containing sample pulses")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    if args.command == "collect":
        settings = Settings.from_env()
        pulses = OTXClient(settings.otx_api_key, settings.otx_base_url).subscribed_pulses(args.limit)
        db = settings.database_path
    else:
        if not args.file:
            parser.error("sample requires --file")
        with open(args.file, encoding="utf-8") as f:
            pulses = json.load(f)
        if not isinstance(pulses, list):
            parser.error("sample JSON must be a list of pulses")
        db = "./threatlens.db"
    store = Store(db)
    try:
        print(json.dumps(ingest(pulses, store), indent=2))
    finally:
        store.close()

if __name__ == "__main__":
    main()

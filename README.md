# ThreatLens

ThreatLens is an analyst-controlled SOC threat intelligence and detection engineering project. **MVP 0.1** collects subscribed AlienVault OTX pulses, validates and normalizes supported IOCs, deduplicates them in SQLite, retains pulse provenance and records ingestion events. All indicators remain `pending_review`.

> **Safety:** No blocking, Elasticsearch writes, rule deployment, or automated approvals. No AI-generated rule execution.

## Quick start (Python 3.11+)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
threatlens sample --file examples/sample_pulses.json
```

To collect real OTX data, copy `.env.example` to `.env`, set your own `OTX_API_KEY`, then run `threatlens collect --limit 10`. Never commit `.env`.

The database is stored in `./threatlens.db` by default. Inspect pending records with `sqlite3 threatlens.db 'select kind,value,status from indicators;'`.

## MVP limitations

Only IPv4, IPv6, domains, HTTP(S) URLs, MD5, SHA1, SHA256 are supported. Non-global IP addresses are rejected. URL hostname checks are conservative; do not fetch IOC URLs. The CLI does not yet have allowlist management, enrichment, scheduled collection, authenticated approval, or detection coverage. OTX subscribed pulses are fetched one page at a time. These are planned, not implemented.

See `docs/architecture.md`, `docs/security.md` and `docs/roadmap.md`.

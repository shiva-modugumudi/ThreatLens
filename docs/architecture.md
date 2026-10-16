# Architecture

OTX subscribed pulses (read-only) -> Python validation/normalization -> SQLite indicators/sightings/audit_events -> pending_review.

The Python CLI owns processing. SQLite ensures unique canonical indicators and unique source-pulse sightings. Each attempted accepted ingestion is audited. Future n8n orchestration will invoke the collector, and a separate authenticated approval service will control exports. Future Elastic Security integration will begin with read-only detection rule inventory.

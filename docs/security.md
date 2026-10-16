# Security boundaries

- OTX keys come from environment variables or a gitignored local `.env` file.
- Never commit secrets, local SQLite databases, or sensitive IOC investigation context.
- All IOC inputs are untrusted. Validation rejects malformed values and non-global IPs.
- Never visit collected URLs or execute collected content.
- All indicators are persisted as `pending_review` only. There is no approval or export implementation in MVP 0.1.
- Database audit entries are local operational records, not tamper-proof audit evidence.
- Run with least-privilege credentials and review outbound connectivity.
- No Elasticsearch integration or rule deployment exists in this milestone.

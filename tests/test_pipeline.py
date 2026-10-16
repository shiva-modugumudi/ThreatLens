from threatlens.cli import ingest
from threatlens.storage import Store

def test_deduplication_and_audit(tmp_path):
    store = Store(str(tmp_path / "test.db"))
    pulses = [{"id": "p1", "indicators": [{"type": "IPv4", "indicator": "8.8.8.8"}]}]
    assert ingest(pulses, store)["created"] == 1
    assert ingest(pulses, store)["duplicate"] == 1
    assert store.connection.execute("SELECT COUNT(*) FROM indicators").fetchone()[0] == 1
    assert store.connection.execute("SELECT COUNT(*) FROM audit_events").fetchone()[0] == 2
    assert store.connection.execute("SELECT status FROM indicators").fetchone()[0] == "pending_review"
    store.close()

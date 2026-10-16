import pytest
from threatlens.validators import normalize_indicator

@pytest.mark.parametrize("kind,value,expected", [
    ("IPv4", "8.8.8.8", "8.8.8.8"),
    ("domain", "EXAMPLE.ORG.", "example.org"),
    ("FileHash-MD5", "A" * 32, "a" * 32),
])
def test_valid(kind, value, expected):
    assert normalize_indicator(kind, value) == (kind, expected)

@pytest.mark.parametrize("kind,value", [("IPv4", "127.0.0.1"), ("IPv4", "10.0.0.1"), ("URL", "file:///etc/passwd"), ("domain", "invalid")])
def test_invalid(kind, value):
    with pytest.raises(ValueError):
        normalize_indicator(kind, value)

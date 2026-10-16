import ipaddress
import re
from urllib.parse import urlsplit, urlunsplit

_HASH_LENGTHS = {"FileHash-MD5": 32, "FileHash-SHA1": 40, "FileHash-SHA256": 64}
_DOMAIN = re.compile(r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z][a-z0-9-]{1,62}$", re.I)

def normalize_indicator(kind: str, value: str) -> tuple[str, str]:
    if not isinstance(kind, str) or not isinstance(value, str):
        raise ValueError("IOC type and value must be strings")
    value = value.strip()
    if len(value) > 2048 or not value:
        raise ValueError("Invalid IOC length")
    if kind in ("IPv4", "IPv6"):
        ip = ipaddress.ip_address(value)
        if ip.version != (4 if kind == "IPv4" else 6):
            raise ValueError("IP version mismatch")
        if not ip.is_global:
            raise ValueError("Non-global IP requires separate review")
        return kind, str(ip)
    if kind in _HASH_LENGTHS:
        if len(value) != _HASH_LENGTHS[kind] or not re.fullmatch(r"[a-fA-F0-9]+", value):
            raise ValueError("Malformed file hash")
        return kind, value.lower()
    if kind == "domain":
        domain = value.rstrip(".").lower()
        if not _DOMAIN.fullmatch(domain):
            raise ValueError("Malformed domain")
        return kind, domain
    if kind == "URL":
        parts = urlsplit(value)
        if parts.scheme.lower() not in ("http", "https") or not parts.hostname or parts.username or parts.password:
            raise ValueError("Only HTTP(S) URLs without credentials are supported")
        if parts.hostname.lower() == "localhost" or not _DOMAIN.fullmatch(parts.hostname):
            raise ValueError("Unsupported URL hostname")
        try:
            port = parts.port
        except ValueError as exc:
            raise ValueError("Malformed URL port") from exc
        host = parts.hostname.lower() + (f":{port}" if port else "")
        return kind, urlunsplit((parts.scheme.lower(), host, parts.path or "/", parts.query, ""))
    raise ValueError(f"Unsupported IOC type: {kind}")

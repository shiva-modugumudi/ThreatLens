import httpx

class OTXClient:
    def __init__(self, api_key: str, base_url: str = "https://otx.alienvault.com"):
        if not api_key:
            raise ValueError("OTX API key required")
        self.base_url = base_url.rstrip("/")
        self.headers = {"X-OTX-API-KEY": api_key, "Accept": "application/json"}

    def subscribed_pulses(self, limit: int = 10) -> list[dict]:
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")
        with httpx.Client(timeout=20, follow_redirects=False) as client:
            response = client.get(f"{self.base_url}/api/v1/pulses/subscribed",
                                  headers=self.headers, params={"limit": limit, "page": 1})
            response.raise_for_status()
            payload = response.json()
        if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
            raise ValueError("Unexpected OTX response format")
        return payload["results"]

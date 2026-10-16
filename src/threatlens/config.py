import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass(frozen=True)
class Settings:
    otx_api_key: str
    database_path: str
    otx_base_url: str

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        key = os.getenv("OTX_API_KEY", "").strip()
        if not key or key == "replace-with-your-key":
            raise ValueError("Set OTX_API_KEY in your local .env file")
        return cls(key, os.getenv("THREATLENS_DB", "./threatlens.db"),
                   os.getenv("OTX_BASE_URL", "https://otx.alienvault.com").rstrip("/"))

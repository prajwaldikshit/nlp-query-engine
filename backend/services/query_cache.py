import time
from typing import Any, Dict, Optional

class QueryCache:
    """
    A simple in-memory cache for storing query results with a Time-To-Live (TTL).
    """
    def __init__(self, ttl_seconds: int = 300):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        """Retrieves an item from the cache if it exists and has not expired."""
        if key not in self._cache:
            return None

        entry = self._cache[key]
        if time.time() > entry['expiry']:
            # The entry has expired, so we delete it and return nothing.
            del self._cache[key]
            return None

        return entry['value']

    def set(self, key: str, value: Any) -> None:
        """Adds an item to the cache with an expiration timestamp."""
        self._cache[key] = {
            'value': value,
            'expiry': time.time() + self.ttl
        }
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class FileReadError(Exception):
    pass

class BaseReader(ABC):
    def __init__(self):
        self.cache = {}

    def cache_content(self, key: str, content: Any):
        self.cache[key] = content

    def get_cached_content(self, key: str) -> Optional[Any]:
        return self.cache.get(key)

    @abstractmethod
    def validate(self, file_path: str) -> bool:
        """Validate if file exists and is readable"""
        pass

    @abstractmethod
    def read(self, file_path: str, password: Optional[str] = None) -> Dict[str, Any]:
        """Read file content with optional password"""
        pass
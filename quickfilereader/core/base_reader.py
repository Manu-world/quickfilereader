from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class FileReadError(Exception):
    """Exception to be raised when a file fails to read"""
    pass

class BaseReader(ABC):
    """Abstract base class for file readers with caching and validation logic"""

    def __init__(self):
        self.cache = {}

    def cache_content(self, key: str, content: Any):
        """Stores content in the cache"""
        self.cache[key] = content

    def get_cached_content(self, key: str) -> Optional[Any]:
        """Retrieves cached content if available"""
        return self.cache.get(key)

    @abstractmethod
    def validate(self, file_path: str) -> bool:
        """Validate if the file exists and is readable"""
        pass

    @abstractmethod
    def read(self, file_path: str, password: Optional[str] = None) -> Dict[str, Any]:
        """Read file content with optional password support"""
        pass
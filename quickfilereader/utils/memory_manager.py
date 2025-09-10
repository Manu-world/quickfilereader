import psutil
from typing import Optional

class MemoryError(Exception):
    """Exception to be raised when memory usage exceeds the limit"""
    pass

class MemoryManager:
    """Singleton class to monitor and handle memory usage"""

    def __init__(self, limit: int = 500 * 1024 * 1024):  # Default limit set to 500MB
        self.limit = limit
        self._instance: Optional['MemoryManager'] = None

    @classmethod
    def get_instance(cls, limit: Optional[int] = None) -> 'MemoryManager':
        """Returns the singleton instance of MemoryManager"""
        if not cls._instance:
            cls._instance = cls(limit if limit else 500 * 1024 * 1024)
        return cls._instance

    def check_memory_usage(self):
        """Checks current memory usage against the set limit"""
        mem = psutil.virtual_memory()
        if mem.used > self.limit:
            raise MemoryError("Memory limit exceeded.")

    def get_current_usage(self) -> int:
        """Returns the current memory usage"""
        return psutil.virtual_memory().used
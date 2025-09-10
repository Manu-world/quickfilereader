import psutil
from typing import Optional

class MemoryError(Exception):
    pass

class MemoryManager:
    def __init__(self, limit: int = 500 * 1024 * 1024):  # Default 500MB
        self.limit = limit
        self._instance: Optional['MemoryManager'] = None

    @classmethod
    def get_instance(cls, limit: Optional[int] = None) -> 'MemoryManager':
        if not cls._instance:
            cls._instance = cls(limit if limit else 500 * 1024 * 1024)
        return cls._instance

    def check_memory_usage(self):
        mem = psutil.virtual_memory()
        if mem.used > self.limit:
            raise MemoryError("Memory limit exceeded.")

    def get_current_usage(self) -> int:
        return psutil.virtual_memory().used
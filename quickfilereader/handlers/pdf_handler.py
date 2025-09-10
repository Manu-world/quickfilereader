import os
from typing import Dict, Any, Optional
import pypdf2
from ..core.base_reader import BaseReader, FileReadError
from ..utils.memory_manager import MemoryManager
import logging

logger = logging.getLogger(__name__)

CHUNK_THRESHOLD = 10  # Determines how many pages are read before caching

class PDFHandler(BaseReader):
    """Handler to read PDF files, with caching and memory management"""

    def __init__(self):
        super().__init__()
        self.memory_manager = MemoryManager.get_instance()

    def validate(self, file_path: str) -> bool:
        """Ensure the PDF exists and is of correct format"""
        if not os.path.exists(file_path):
            logger.error(f"Validation failed: File {file_path} not found")
            raise FileReadError(f"File not found: {file_path}")
        if not file_path.lower().endswith('.pdf'):
            logger.error("Validation failed: Invalid file format. Expected PDF")
            raise FileReadError("Invalid file format. Expected PDF")
        return True

    def read(self, file_path: str, password: Optional[str] = None) -> Dict[str, Any]:
        """Read contents from a PDF file, with password protection if needed"""
        self.validate(file_path)
        content, metadata = [], {}
        
        try:
            with open(file_path, 'rb') as file:
                reader = pypdf2.PdfReader(file)
                
                if reader.is_encrypted and password:
                    reader.decrypt(password)
                elif reader.is_encrypted and not password:
                    logger.error("Read failed: PDF is encrypted but no password provided")
                    raise FileReadError("PDF is encrypted but no password provided")

                # Extract metadata
                metadata = {
                    'pages': len(reader.pages),
                    'encrypted': reader.is_encrypted,
                }

                # Process pages with memory checks
                for page_num, page in enumerate(reader.pages):
                    self.memory_manager.check_memory_usage()
                    page_content = page.extract_text()
                    content.append(page_content)

                    # Cache once the CHUNK_THRESHOLD is met
                    if len(content) >= CHUNK_THRESHOLD:
                        cache_key = f"{file_path}_pages_{page_num-CHUNK_THRESHOLD}_{page_num}"
                        self.cache_content(cache_key, content)
                        content = []

        except Exception as e:
            logger.error(f"Read failed: {str(e)}")
            raise FileReadError(f"Failed to read PDF: {str(e)}")

        # Cache remaining content
        if content:
            cache_key = f"{file_path}_pages_final"
            self.cache_content(cache_key, content)

        logger.info(f"PDF {file_path} read successfully with metadata: {metadata}")

        return {
            'content': self.get_all_content(file_path),
            'metadata': metadata
        }

    def get_all_content(self, file_path: str) -> str:
        """Aggregate all cached contents related to the file"""
        all_content = []
        for key in sorted(self.cache):
            if key.startswith(file_path):
                all_content.extend(self.cache[key])
        return '\n'.join(all_content)
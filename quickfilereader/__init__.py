import os
import logging
import pandas as pd
import PyPDF2
from spire.doc import Document, DocumentObjectType
from typing import Union, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_pdf(file_path: str, start_page: int = 0, end_page: Optional[int] = None) -> str:
    """
    Read content from a PDF file.
    
    Args:
        file_path (str): Path to the PDF file
        start_page (int, optional): Starting page to read. Defaults to 0.
        end_page (Optional[int], optional): Ending page to read. Defaults to None (read all pages).
    
    Returns:
        str: Extracted PDF text
    """
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Validate page range
            total_pages = len(pdf_reader.pages)
            
            if start_page < 0 or start_page >= total_pages:
                raise ValueError(f"Invalid start page. Must be between 0 and {total_pages - 1}")
            
            # Adjust end_page
            end_page = end_page or total_pages
            end_page = min(end_page, total_pages)
            
            # Extract text from specified page range
            extracted_text = [
                pdf_reader.pages[page_num].extract_text() 
                for page_num in range(start_page, end_page)
            ]
            
            return '\n'.join(extracted_text)
    
    except Exception as e:
        logging.error(f"Error reading PDF {file_path}: {e}")
        raise

def read_txt(file_path: str) -> str:
    """
    Read content from a text file.
    
    Args:
        file_path (str): Path to the text file
    
    Returns:
        str: File contents
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        logging.error(f"Error reading text file {file_path}: {e}")
        raise

def read_docs(file_path: str) -> str:
    """
    Read content from a Word document.
    
    Args:
        file_path (str): Path to the Word document
    
    Returns:
        str: Extracted document text
    """
    try:
        doc = Document()
        doc.LoadFromFile(file_path)
        
        combined_content = []
        for i in range(doc.Sections.Count):
            section = doc.Sections.get_Item(i)
            section_content = []
            
            for j in range(section.Body.ChildObjects.Count):
                element = section.Body.ChildObjects.get_Item(j)
                
                if element.DocumentObjectType == DocumentObjectType.Paragraph:
                    section_content.append(element.Text)
                
                elif element.DocumentObjectType == DocumentObjectType.Table:
                    table_rows = []
                    for m in range(element.Rows.Count):
                        row_data = [
                            element.Rows.get_Item(m).Cells.get_Item(n).Paragraphs.get_Item(0).Text 
                            for n in range(element.Rows.get_Item(m).Cells.Count)
                        ]
                        table_rows.append(" | ".join(row_data))
                    section_content.extend(table_rows)
            
            combined_content.append("\n".join(section_content))
        
        return "\n\n".join(combined_content)
    
    except Exception as e:
        logging.error(f"Error reading Word document {file_path}: {e}")
        raise

def read_excel(file_path: str) -> str:
    """
    Read content from an Excel file.
    
    Args:
        file_path (str): Path to the Excel file
    
    Returns:
        str: Excel file contents as a string
    """
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        return df.to_string(index=False)
    except Exception as e:
        logging.error(f"Error reading Excel file {file_path}: {e}")
        raise

def read_csv(file_path: str) -> str:
    """
    Read content from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file
    
    Returns:
        str: CSV file contents as a string
    """
    try:
        df = pd.read_csv(file_path)
        return df.to_string(index=False)
    except Exception as e:
        logging.error(f"Error reading CSV file {file_path}: {e}")
        raise

def read_any_file(file_path: str, start_page: int = 0, end_page: Optional[int] = None) -> Union[str, None]:
    """
    Read file content automatically based on file extension.
    
    Args:
        file_path (str): Path to the file
        start_page (int, optional): Starting page for PDF files
        end_page (Optional[int], optional): Ending page for PDF files
    
    Returns:
        str: File contents
    
    Raises:
        ValueError: If file type is not supported
    """
    # Validate file existence
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Get file extension
    file_extension = os.path.splitext(file_path)[1].lower()
    
    # Map extensions to reading functions
    file_readers = {
        '.pdf': read_pdf,
        '.txt': read_txt,
        '.docx': read_docs,
        '.doc': read_docs,
        '.xlsx': read_excel,
        '.xls': read_excel,
        '.csv': read_csv
    }
    
    # Select appropriate reader
    reader = file_readers.get(file_extension)
    
    if not reader:
        raise ValueError(f"Unsupported file type: {file_extension}")
    
    # Call the appropriate reader function
    if file_extension == '.pdf':
        return reader(file_path, start_page, end_page)
    return reader(file_path)

# Expose individual file reading functions and the general file reader
__all__ = [
    'read_pdf', 
    'read_txt', 
    'read_docs', 
    'read_excel', 
    'read_csv', 
    'read_any_file'
]
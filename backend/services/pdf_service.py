import logging
from pathlib import Path
import pypdf

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path):
    """
    Extract readable text from a PDF document using pypdf.
    Returns:
        dict: {
            "success": bool,
            "text": str,
            "page_count": int,
            "is_scanned": bool,
            "error": str (optional)
        }
    """
    try:
        path = Path(pdf_path)
        if not path.exists():
            return {"success": False, "error": f"File not found: {pdf_path}"}
            
        reader = pypdf.PdfReader(str(path))
        num_pages = len(reader.pages)
        full_text = []
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            clean_text = text.strip()
            if clean_text:
                full_text.append(f"--- Page {i + 1} ---\n{clean_text}")
                
        joined_text = "\n\n".join(full_text).strip()
        
        # Check if PDF contains extracted text or is purely scanned images
        is_scanned = len(joined_text) < 50
        
        return {
            "success": True,
            "text": joined_text,
            "page_count": num_pages,
            "is_scanned": is_scanned,
            "word_count": len(joined_text.split())
        }
    except Exception as e:
        logger.error(f"Error reading PDF {pdf_path}: {e}")
        return {
            "success": False,
            "error": f"Failed to extract text from PDF: {str(e)}",
            "text": "",
            "page_count": 0,
            "is_scanned": True
        }

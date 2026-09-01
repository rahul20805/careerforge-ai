import re
import httpx
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional
import fitz  # PyMuPDF
from docx import Document as DocxDocument

from app.ai.router import ai_service


class JDParser:
    """
    Robust Job & Research Description Parser.
    Accepts Raw Text, URL, PDF file path, or DOCX file path.
    """

    @classmethod
    async def parse_text(cls, text: str) -> Dict[str, Any]:
        return await ai_service.extract_job_details(text)

    @classmethod
    async def parse_url(cls, url: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CareerForgeAI/1.0"}
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                raise ValueError(f"Unable to fetch URL. HTTP status {response.status_code}")
                
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Remove scripts and styles
            for element in soup(["script", "style", "nav", "footer", "header", "noscript"]):
                element.extract()
                
            clean_text = soup.get_text(separator="\n")
            lines = [line.strip() for line in clean_text.splitlines() if line.strip()]
            extracted_text = "\n".join(lines)
            
            parsed = await ai_service.extract_job_details(extracted_text)
            parsed["source_url"] = url
            parsed["official_url"] = url
            return parsed

    @classmethod
    async def parse_pdf(cls, file_bytes: bytes) -> Dict[str, Any]:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text_parts = []
        for page in doc:
            text_parts.append(page.get_text())
        extracted_text = "\n".join(text_parts)
        return await ai_service.extract_job_details(extracted_text)

    @classmethod
    async def parse_docx(cls, file_path: str) -> Dict[str, Any]:
        doc = DocxDocument(file_path)
        text_parts = [p.text for p in doc.paragraphs if p.text.strip()]
        extracted_text = "\n".join(text_parts)
        return await ai_service.extract_job_details(extracted_text)

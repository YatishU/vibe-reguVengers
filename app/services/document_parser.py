import fitz  # PyMuPDF
import io
from typing import Optional, Dict, Any
import re
from fastapi import UploadFile
import aiofiles
import os
from pathlib import Path

class DocumentParser:
    def __init__(self):
        self.supported_formats = ['.pdf']
        self.max_file_size = 50 * 1024 * 1024  # 50MB
        
    async def parse_pdf(self, file: UploadFile) -> str:
        """Parse PDF file and extract text content"""
        try:
            # Read file content
            content = await file.read()
            
            # Validate file size
            if len(content) > self.max_file_size:
                raise ValueError(f"File size exceeds maximum limit of {self.max_file_size} bytes")
            
            # Parse PDF using PyMuPDF
            pdf_document = fitz.open(stream=content, filetype="pdf")
            
            extracted_text = ""
            
            # Extract text from each page
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                text = page.get_text()
                extracted_text += text + "\n"
            
            pdf_document.close()
            
            # Clean and normalize text
            cleaned_text = self._clean_text(extracted_text)
            
            return cleaned_text
            
        except Exception as e:
            print(f"Error parsing PDF: {str(e)}")
            raise ValueError(f"Failed to parse PDF file: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and headers
        text = re.sub(r'Page \d+ of \d+', '', text)
        text = re.sub(r'\d+/\d+', '', text)
        
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\{\}]', '', text)
        
        # Normalize line breaks
        text = text.replace('\n', ' ').replace('\r', ' ')
        
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)
        
        return text.strip()
    
    async def extract_metadata(self, file: UploadFile) -> Dict[str, Any]:
        """Extract metadata from PDF file"""
        try:
            content = await file.read()
            pdf_document = fitz.open(stream=content, filetype="pdf")
            
            metadata = {
                "page_count": pdf_document.page_count,
                "file_size": len(content),
                "filename": file.filename,
                "content_type": file.content_type
            }
            
            # Try to extract document metadata
            try:
                doc_metadata = pdf_document.metadata
                metadata.update({
                    "title": doc_metadata.get("title", ""),
                    "author": doc_metadata.get("author", ""),
                    "subject": doc_metadata.get("subject", ""),
                    "creator": doc_metadata.get("creator", ""),
                    "producer": doc_metadata.get("producer", ""),
                    "creation_date": doc_metadata.get("creationDate", ""),
                    "modification_date": doc_metadata.get("modDate", "")
                })
            except:
                pass
            
            pdf_document.close()
            
            return metadata
            
        except Exception as e:
            print(f"Error extracting metadata: {str(e)}")
            return {
                "filename": file.filename,
                "file_size": len(content) if 'content' in locals() else 0,
                "error": str(e)
            }
    
    async def extract_tables(self, file: UploadFile) -> list:
        """Extract tables from PDF file"""
        try:
            content = await file.read()
            pdf_document = fitz.open(stream=content, filetype="pdf")
            
            tables = []
            
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                
                # Extract tables from page
                page_tables = page.get_tables()
                
                for table in page_tables:
                    tables.append({
                        "page": page_num + 1,
                        "data": table
                    })
            
            pdf_document.close()
            
            return tables
            
        except Exception as e:
            print(f"Error extracting tables: {str(e)}")
            return []
    
    async def extract_images(self, file: UploadFile) -> list:
        """Extract images from PDF file"""
        try:
            content = await file.read()
            pdf_document = fitz.open(stream=content, filetype="pdf")
            
            images = []
            
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                
                # Extract images from page
                image_list = page.get_images()
                
                for img_index, img in enumerate(image_list):
                    try:
                        xref = img[0]
                        pix = fitz.Pixmap(pdf_document, xref)
                        
                        if pix.n - pix.alpha < 4:  # GRAY or RGB
                            images.append({
                                "page": page_num + 1,
                                "index": img_index,
                                "width": pix.width,
                                "height": pix.height,
                                "colorspace": pix.colorspace.name
                            })
                        
                        pix = None
                        
                    except Exception as img_error:
                        print(f"Error processing image {img_index} on page {page_num}: {str(img_error)}")
                        continue
            
            pdf_document.close()
            
            return images
            
        except Exception as e:
            print(f"Error extracting images: {str(e)}")
            return []
    
    def validate_file(self, file: UploadFile) -> bool:
        """Validate uploaded file"""
        # Check file extension
        if not any(file.filename.lower().endswith(ext) for ext in self.supported_formats):
            return False
        
        # Check content type
        if file.content_type not in ['application/pdf']:
            return False
        
        return True
    
    async def save_file(self, file: UploadFile, directory: str = "uploads") -> str:
        """Save uploaded file to disk"""
        try:
            # Create directory if it doesn't exist
            Path(directory).mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename
            timestamp = int(time.time())
            filename = f"{timestamp}_{file.filename}"
            filepath = os.path.join(directory, filename)
            
            # Save file
            async with aiofiles.open(filepath, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            return filepath
            
        except Exception as e:
            print(f"Error saving file: {str(e)}")
            raise ValueError(f"Failed to save file: {str(e)}")

import time 
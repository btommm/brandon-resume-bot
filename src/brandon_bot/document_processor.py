"""
Document processing module for Brandon Resume Bot
Handles PDF, DOCX, and text file processing
"""

import os
import json
from typing import List, Dict, Optional
import PyPDF2
import docx
from .config import config

class DocumentProcessor:
    """Process and manage resume and portfolio documents"""
    
    def __init__(self):
        self.documents = {}
        self.processed_content = ""
        
    def load_all_documents(self) -> Dict[str, str]:
        """Load all documents from the data directory"""
        documents = {}
        data_dir = config.DATA_DIR
        
        if os.path.exists(data_dir):
            documents.update(self._scan_directory(data_dir))
        else:
            print(f"Warning: {data_dir} directory not found")
        
        self.documents = documents
        self.processed_content = self._combine_documents(documents)
        return documents
    
    def _scan_directory(self, directory: str) -> Dict[str, str]:
        """Scan a directory for supported document files"""
        documents = {}
        
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            # Skip directories and README files
            if os.path.isdir(file_path) or filename.lower() == 'readme.md':
                continue
            
            if filename.endswith('.pdf'):
                content = self._extract_pdf(file_path)
            elif filename.endswith('.docx'):
                content = self._extract_docx(file_path)
            elif filename.endswith('.txt'):
                content = self._extract_text(file_path)
            elif filename.endswith('.md'):
                content = self._extract_text(file_path)
            elif filename.endswith('.json'):
                content = self._extract_json(file_path)
            else:
                continue
                
            if content:
                documents[filename] = content
                print(f"✅ Loaded: {filename}")
            else:
                print(f"❌ Failed to load: {filename}")
                
        return documents
    
    def _extract_pdf(self, file_path: str) -> Optional[str]:
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            return None
    
    def _extract_docx(self, file_path: str) -> Optional[str]:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = []
            for paragraph in doc.paragraphs:
                text.append(paragraph.text)
            return "\n".join(text)
        except Exception as e:
            print(f"Error reading DOCX {file_path}: {e}")
            return None
    
    def _extract_text(self, file_path: str) -> Optional[str]:
        """Extract text from TXT or MD file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading text file {file_path}: {e}")
            return None
    
    def _extract_json(self, file_path: str) -> Optional[str]:
        """Extract and format JSON data"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # Convert JSON to readable text format
                return json.dumps(data, indent=2)
        except Exception as e:
            print(f"Error reading JSON file {file_path}: {e}")
            return None
    
    def _combine_documents(self, documents: Dict[str, str]) -> str:
        """Combine all documents into a single context string"""
        combined = []
        
        for filename, content in documents.items():
            combined.append(f"=== {filename.upper()} ===")
            combined.append(content)
            combined.append("\n" + "="*50 + "\n")
        
        return "\n".join(combined)
    
    
    def get_document_summary(self) -> str:
        """Get a summary of loaded documents"""
        if not self.documents:
            return "No documents loaded."
        
        summary = [f"Loaded {len(self.documents)} documents:"]
        for filename in self.documents.keys():
            summary.append(f"- {filename}")
        
        return "\n".join(summary)

# Global document processor instance
document_processor = DocumentProcessor()

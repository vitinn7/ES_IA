import os
from utils.helpers import extract_text_from_pdf

class PDFContextLoader:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def load_context(self):
        """Carrega o texto de todos os PDFs na pasta especificada."""
        pdf_texts = []
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(self.folder_path, filename)
                pdf_texts.append(extract_text_from_pdf(file_path))
        return " ".join(pdf_texts)

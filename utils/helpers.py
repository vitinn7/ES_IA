import PyPDF2

def extract_text_from_pdf(file_path):
    """Extrai texto de um arquivo PDF."""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
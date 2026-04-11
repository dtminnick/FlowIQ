
import docx
# import PyPDF2
from pypdf import PdfReader


class FileReader:
    def read(self, filepath: str) -> str:
        if filepath.lower().endswith(".docx"):
            return self._read_docx(filepath)
        elif filepath.lower().endswith(".pdf"):
            return self._read_pdf(filepath)
        else:
            raise ValueError(f"Unsupported file type: {filepath}")

    def _read_docx(self, filepath: str) -> str:
        doc = docx.Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])

    def _read_pdf(self, filepath: str) -> str:
        text = []
        with open(filepath, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text.append(page.extract_text() or "")
        return "\n".join(text)

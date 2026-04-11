
from pathlib import Path

class FileWriter:
    def __init__(self, base_dir: str = "data/outputs"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_text(self, text: str, filename: str) -> Path:
        file_path = self.base_dir / filename

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)

        return file_path
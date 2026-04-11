import unicodedata
import re

class Cleaner:
    def __init__(self, config = None):
        self.config = config or {}
        self.steps = [
            self._normalize_unicode,
            self._fix_line_breaks,
            self._collapse_repeated_whitespace,
            self._standardize_bullets,
        ]

        if self.config.get("tag_urls", True):
            self.steps.append(self._tag_urls)

        self.steps.extend([
            self._remove_emails,
            self._normalize_punctuation,
            self._remove_bracketed,
            self._remove_emojis,
            self._normalize_repeated_punctuation,
            self._remove_nonprintable,
            self._strip_whitespace
        ])

    def clean(self, text: str) -> str:
        for step in self.steps:
            text = step(text)

        return text
    
    def _strip_whitespace(self, text: str) -> str:
        return text.strip()
    
    def _normalize_unicode(self, text: str) -> str:
        return unicodedata.normalize("NFKC", text)
    
    def _fix_line_breaks(self, text: str) -> str:
        return text.replace("\r\n", "\n").replace("\r", "\n")

    def _collapse_repeated_whitespace(self, text: str) -> str:
        # Collapse multiple spaces/tabs
        text = re.sub(r"[ \t]+", " ", text)
    
        # Collapse 3+ newlines into 2
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text
    
    def _standardize_bullets(self, text: str) -> str:
        return text.replace("•", "-").replace("·", "-").replace("*", "-")
    
    def _tag_urls(self, text: str) -> str:
        url_pattern = r"(https?://\S+|www\.\S+)"
        
        def replacer(match):
            url = match.group(0)
            return f"[URL:{url}]"
        
        return re.sub(url_pattern, replacer, text)

    def _remove_emails(self, text: str) -> str:
        email_pattern = r"\b[\w\.-]+@[\w\.-]+\.\w+\b"
        return re.sub(email_pattern, "", text)

    def _normalize_punctuation(self, text: str) -> str:
        replacements = {
            "“": '"', "”": '"',
            "‘": "'", "’": "'",
            "—": "-", "–": "-",
            "…": "...",
        }

        for k, v in replacements.items():
            text = text.replace(k, v)
        return text

    def _remove_bracketed(self, text: str) -> str:
        # Remove (), {} but NOT square brackets (we use them for tags)
        text = re.sub(r"\(.*?\)", "", text)
        text = re.sub(r"\{.*?\}", "", text)
        return text

    def _remove_emojis(self, text: str) -> str:
        emoji_pattern = r"[\U00010000-\U0010ffff]"
        return re.sub(emoji_pattern, "", text)

    def _normalize_repeated_punctuation(self, text: str) -> str:
        # Collapse repeated punctuation: !!! → !, ---- → -, etc.
        return re.sub(r"([!?.\-])\1+", r"\1", text)

    def _remove_nonprintable(self, text: str) -> str:
        return "".join(ch for ch in text if ch.isprintable() or ch == "\n")

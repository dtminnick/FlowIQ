import unicodedata
import re

class Cleaner:
    def __init__(self, config = None):
        self.config = config or {}
        self.steps = [
            self._strip_whitespace,
            self._normalize_unicode,
            self._fix_line_breaks,
            self._collapse_repeated_whitespace,
            self._standardize_bullets,
            self._remove_urls,
            self._remove_emails,
            self._normalize_punctuation,
            self._remove_bracketed,
            self._remove_emojis,
            self._normalize_repeated_punctuation,
            self._remove_nonprintable
        ]

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
        return re.sub(r"\n{3,}", "\n\n", text)
    
    def _standardize_bullets(self, text: str) -> str:
        return text.replace("•", "-").replace("·", "-").replace("*", "-")
    
    def _remove_urls(self, text: str) -> str:
        url_pattern = r"https?://\S+|www\.\S+"
        return re.sub(url_pattern, "", text)

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
        # Removes (...) [...] {...}
        return re.sub(r"[\(\[\{].*?[\)\]\}]", "", text)

    def _remove_emojis(self, text: str) -> str:
        emoji_pattern = r"[\U00010000-\U0010ffff]"
        return re.sub(emoji_pattern, "", text)

    def _normalize_repeated_punctuation(self, text: str) -> str:
        # Collapse repeated punctuation: !!! → !, ---- → -, etc.
        return re.sub(r"([!?.\-])\1+", r"\1", text)

    def _remove_nonprintable(self, text: str) -> str:
        return "".join(ch for ch in text if ch.isprintable())

import unicodedata
import re
import yaml
import os

class Cleaner:
    def __init__(self, config = None):
        self.config = config or {}

        config_path = self.config.get("verbs_path", "config/verbs.yaml")

        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                verb_config = yaml.safe_load(f)
                self.common_verbs = set(verb_config.get("common_verbs", []))
        else:
            self.common_verbs = set()

        with open("config/headers.yaml", "r") as f:
            self.header_rules = yaml.safe_load(f)["header_rules"]

        self.steps = [
            self._normalize_unicode,
            self._fix_line_breaks,
            self._collapse_repeated_whitespace,
            self._strip_whitespace,
            self._standardize_bullets,
            self._enforce_step_structure,
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
            self._remove_empty_lines
        ])

    def clean(self, text: str) -> str:
        for step in self.steps:
            text = step(text)

        # Now split into lines for checklist normalization
        lines = text.split("\n")
        lines = self._normalize_checklists(lines)

        # Rejoin
        text = "\n".join(lines)

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
    
    def _enforce_step_structure(self, text: str) -> str:
        lines = text.split("\n")
        updated = []

        for line in lines:
            stripped = line.strip()

            if not stripped:
                updated.append(line)
                continue

            # Already a bullet → keep
            if stripped.startswith("-"):
                updated.append(line)
                continue

            # Skip obvious headers (ALL CAPS, short)
            if self._is_header(stripped):
                updated.append(line)
                continue

            # Detect step-like lines
            if self._looks_like_step(stripped):
                updated.append(f"- {stripped}")
            else:
                updated.append(line)

        return "\n".join(updated)
    
    def _is_header(self, line: str) -> bool:
        rules = self.header_rules
        stripped = line.strip()

        # Word count rule
        if len(stripped.split()) > rules["max_words"]:
            return False

        # ALL CAPS rule
        if rules["detect_all_caps"] and stripped.isupper():
            return True

        # Title Case rule
        if rules["detect_title_case"] and stripped.istitle():
            return True

        # Colon suffix rule
        if rules["detect_colon_suffix"] and stripped.endswith(":"):
            return True

        # Keyword rule
        if stripped.lower() in rules.get("keywords", []):
            return True

        # No-verb rule
        first_word = stripped.split()[0].lower()
        if rules["detect_no_verb"] and first_word not in self.common_verbs:
            return True

        return False

    def _looks_like_step(self, line: str) -> bool:
        # Starts with a verb-like word (simple heuristic)
        first_word = line.split()[0].lower()

        if first_word in self.common_verbs:
            return True

        # Lines starting with "if" → decision steps
        if line.lower().startswith("if "):
            return True

        # Lines ending with a period and reasonably short → likely step
        if line.endswith(".") and len(line.split()) < 25:
            return True

        return False
    
    def _remove_empty_lines(self, text: str) -> str:
        lines = text.split("\n")
        cleaned = []
        prev_blank = False

        for line in lines:
            if not line.strip():
                # allow a single blank line, but not multiple
                if not prev_blank:
                    cleaned.append("")
                prev_blank = True
            else:
                cleaned.append(line)
                prev_blank = False

        return "\n".join(cleaned)

    def _standardize_bullets(self, text: str) -> str:
        # Common bullet characters
        bullet_chars = r"[•·*o→]"
        text = re.sub(rf"^\s*{bullet_chars}\s+", "- ", text, flags=re.MULTILINE)

        # Numbered bullets
        text = re.sub(r"^\s*\d+[\.\)]\s+", "- ", text, flags=re.MULTILINE)

        # Lettered bullets
        text = re.sub(r"^\s*[A-Za-z][\.\)]\s+", "- ", text, flags=re.MULTILINE)

        return text

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
    
    def _normalize_checklists(self, lines):
        import re

        output = []
        i = 0

        while i < len(lines):
            line = lines[i]

            # Detect a checklist header
            if re.search(r'\bCHECKLIST\b', line, re.IGNORECASE):
                output.append(line)
                i += 1

                checklist_block = []

                while i < len(lines):
                    item = lines[i].strip()

                    # Stop if blank or next header/section
                    if not item:
                        break

                    # Stop if already bulleted or numbered
                    if re.match(r'^[-*•]\s+', item) or re.match(r'^\d+[\.\)]\s+', item):
                        break

                    # Stop if punctuation suggests it's not a checklist item
                    if re.search(r'[.,:;!?()\[\]]', item):
                        break

                    # Stop if not capitalized
                    if not re.match(r'^[A-Z]', item):
                        break

                    checklist_block.append(item)
                    i += 1

                # Convert only if we found at least 2 items
                if len(checklist_block) >= 2:
                    for item in checklist_block:
                        output.append(f"- {item}")
                else:
                    for item in checklist_block:
                        output.append(item)

            else:
                output.append(line)
                i += 1

        return output

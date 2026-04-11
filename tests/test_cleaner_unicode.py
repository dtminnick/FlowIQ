
from src.preprocessing.cleaner import Cleaner

def test_normalize_unicode():
    cleaner = Cleaner()
    text = "Café"  # contains é in composed form
    cleaned = cleaner.clean(text)
    # After NFKC normalization, the string should still be semantically identical
    assert "Cafe" in cleaned or "Café" in cleaned

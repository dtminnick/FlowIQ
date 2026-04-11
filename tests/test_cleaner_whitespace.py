
from src.preprocessing.cleaner import Cleaner

def test_collapse_repeated_whitespace():
    cleaner = Cleaner()
    text = "Line1\n\n\n\nLine2"
    cleaned = cleaner.clean(text)
    # Should collapse 4 newlines into 2
    assert "\n\n\n" not in cleaned
    assert "\n\n" in cleaned

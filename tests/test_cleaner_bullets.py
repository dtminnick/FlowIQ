
from src.preprocessing.cleaner import Cleaner

def test_standardize_bullets():
    cleaner = Cleaner()
    text = "• Step one\n* Step two\n- Step three"
    cleaned = cleaner.clean(text)
    assert cleaned.count("-") == 3
    assert "•" not in cleaned
    assert "*" not in cleaned

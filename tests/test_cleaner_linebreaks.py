
from src.preprocessing.cleaner import Cleaner

def test_fix_line_breaks():
    cleaner = Cleaner()
    text = "Line1\r\nLine2\rLine3\nLine4"
    cleaned = cleaner.clean(text)
    assert cleaned.count("\r") == 0
    assert cleaned.count("\n") == 3

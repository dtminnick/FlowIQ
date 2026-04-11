
from src.preprocessing.cleaner import Cleaner

def test_strip_whitespace():
    cleaner = Cleaner()
    text = "   Hello world   "
    cleaned = cleaner.clean(text)
    assert cleaned == "Hello world"

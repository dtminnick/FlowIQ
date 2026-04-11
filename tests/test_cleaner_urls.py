
from src.preprocessing.cleaner import Cleaner

def test_remove_urls():
    c = Cleaner()
    assert c.remove_urls("Visit https://example.com now") == "Visit "

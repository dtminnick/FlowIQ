
from src.preprocessing.cleaner import Cleaner

def test_tag_urls():
    c = Cleaner()
    assert c._tag_urls("Visit https://example.com now") == "Visit [URL:https://example.com] now"

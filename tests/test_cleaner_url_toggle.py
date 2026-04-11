
from src.preprocessing.cleaner import Cleaner

def test_url_tagging_toggle():
    text = "Visit https://example.com"

    c1 = Cleaner()
    assert "[URL:https://example.com]" in c1.clean(text)

    c2 = Cleaner(config={"tag_urls": False})
    assert "[URL:" not in c2.clean(text)

from src.preprocessing.cleaner import Cleaner

def run_cleaner_tests():
    cleaner = Cleaner()

    test_inputs = [
        "   Leading and trailing spaces   ",
        "\n\nMultiple\n\nNewlines\n\n",
        "Mixed   spacing   inside   text",
        "Tabs\tand spaces   together",
        "   ",
        "",
        "Already clean text."
    ]

    for i, text in enumerate(test_inputs, start=1):
        cleaned = cleaner.clean(text)
        print(f"\n--- Test {i} ---")
        print(f"Input:  {repr(text)}")
        print(f"Output: {repr(cleaned)}")

if __name__ == "__main__":
    run_cleaner_tests()

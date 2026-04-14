from src.preprocessing.cleaner import Cleaner

def test_normalize_checklist_minimal():
    cleaner = Cleaner()

    input_text = "\n".join([
        "PRE-PROCESSING CHECKLIST",
        "Employee personnel file",
        "Retirement eligibility calculator",
        "Access to Payroll System",
        ""
    ])

    expected_lines = [
        "PRE-PROCESSING CHECKLIST",
        "- Employee personnel file",
        "- Retirement eligibility calculator",
        "- Access to Payroll System"
    ]

    cleaned = cleaner.clean(input_text)
    cleaned_lines = cleaned.split("\n")

    assert cleaned_lines == expected_lines

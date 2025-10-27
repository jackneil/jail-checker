import pdfplumber
import re

def expand_case_range(case_number):
    """
    Expand a case number range into individual case numbers.

    Examples:
        2025GS1801261-01265 -> [2025GS1801261, 2025GS1801262, 2025GS1801263, 2025GS1801264, 2025GS1801265]
        2023GS18-02066 -> [2023GS18-02066]
    """
    # Check if this is a range (has two numbers separated by dash at the end)
    match = re.match(r'(\d+GS\d+)(\d+)-(\d+)$', case_number)

    if not match:
        # Not a range, return as-is
        return [case_number]

    prefix = match.group(1)
    start_num = int(match.group(2))
    end_num = int(match.group(3))

    # Generate all numbers in range
    expanded = []
    for num in range(start_num, end_num + 1):
        # Pad with zeros to match original length
        num_str = str(num).zfill(len(match.group(2)))
        expanded.append(f"{prefix}{num_str}")

    return expanded


pdf = pdfplumber.open(r'C:\Github\jail-checker\input\Prosecutor Worklist Report.pdf')

all_case_numbers = []

for page in pdf.pages:
    words = page.extract_words()

    # Find all case numbers
    case_words = [
        w['text'].rstrip(',') for w in words
        if 'GS' in w['text'] and 100 < w['x0'] < 200
    ]

    all_case_numbers.extend(case_words)

pdf.close()

# Get unique case numbers
unique_case_numbers = list(dict.fromkeys(all_case_numbers))

print(f'Unique case number entries found: {len(unique_case_numbers)}')

# Expand ranges
all_individual_cases = []
range_cases = []

for case in unique_case_numbers:
    expanded = expand_case_range(case)
    all_individual_cases.extend(expanded)

    if len(expanded) > 1:
        range_cases.append({
            'original': case,
            'expanded': expanded,
            'count': len(expanded)
        })

print(f'Total individual cases (after expanding ranges): {len(all_individual_cases)}')
print(f'\nCase ranges found: {len(range_cases)}')
for r in range_cases:
    print(f'  {r["original"]:30s} -> {r["count"]} cases')
    print(f'    {", ".join(r["expanded"])}')

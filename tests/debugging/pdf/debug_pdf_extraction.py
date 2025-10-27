import sys
sys.path.insert(0, r'C:\Github\jail-checker\src')

import pdfplumber
from parsers import parse_defendant_name

pdf = pdfplumber.open(r'C:\Github\jail-checker\input\Prosecutor Worklist Report.pdf')

total_case_entries = 0
total_defendants_extracted = 0
failed_extractions = []

for page_num, page in enumerate(pdf.pages, 1):
    words = page.extract_words()

    # Find case numbers
    case_words = [
        w for w in words
        if 'GS' in w['text']
        and 100 < w['x0'] < 200
        and any(year in w['text'] for year in ['2022', '2023', '2024', '2025'])
    ]

    total_case_entries += len(case_words)

    for case in case_words:
        # Find defendant name
        defendant_words = [
            w for w in words
            if abs(w['top'] - case['top']) < 1
            and 210 < w['x0'] < 360
        ]

        if not defendant_words:
            failed_extractions.append({
                'page': page_num,
                'case_number': case['text'],
                'reason': 'No defendant words found in name column'
            })
            continue

        defendant_words_sorted = sorted(defendant_words, key=lambda x: x['x0'])
        defendant_name = ' '.join([w['text'] for w in defendant_words_sorted])

        # Check if name has both first and last
        first, middle, last = parse_defendant_name(defendant_name)

        if not (first and first.strip() and last and last.strip()):
            failed_extractions.append({
                'page': page_num,
                'case_number': case['text'],
                'defendant_name': defendant_name,
                'first': first,
                'last': last,
                'reason': 'Missing first or last name after parsing'
            })
            continue

        total_defendants_extracted += 1

pdf.close()

print(f'Total case number entries found: {total_case_entries}')
print(f'Total defendants successfully extracted: {total_defendants_extracted}')
print(f'Failed extractions: {len(failed_extractions)}')

if failed_extractions:
    print('\n' + '='*80)
    print('FAILED EXTRACTIONS:')
    print('='*80)
    for fail in failed_extractions:
        print(f"\nPage {fail['page']} | Case: {fail['case_number']}")
        print(f"  Reason: {fail['reason']}")
        if 'defendant_name' in fail:
            print(f"  Defendant Name: {fail['defendant_name']}")
            print(f"  Parsed: first='{fail['first']}', last='{fail['last']}'")

import pdfplumber

pdf = pdfplumber.open(r'C:\Github\jail-checker\input\Prosecutor Worklist Report.pdf')
page = pdf.pages[1]
words = page.extract_words()

# Find case numbers
case_words = [w for w in words if '2023GS' in w['text'] or '2024GS' in w['text']]

print(f'Found {len(case_words)} case numbers on page 2')
print('\nFor each case number, extract defendant name from same row:\n')

for case in case_words:
    # Find all words on the same row (same top position, within 1 point tolerance)
    same_row = [w for w in words if abs(w['top'] - case['top']) < 1]

    # Sort by x position
    same_row_sorted = sorted(same_row, key=lambda x: x['x0'])

    # Defendant name should be around x0=216.9
    defendant_words = [w for w in same_row if 210 < w['x0'] < 360]
    defendant_name = ' '.join([w['text'] for w in sorted(defendant_words, key=lambda x: x['x0'])])

    print(f"Case: {case['text']:25s} Defendant: {defendant_name}")

pdf.close()

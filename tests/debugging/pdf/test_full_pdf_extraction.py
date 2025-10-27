import pdfplumber

pdf = pdfplumber.open(r'C:\Github\jail-checker\input\Prosecutor Worklist Report.pdf')

all_defendants = []

for page_num, page in enumerate(pdf.pages, 1):
    words = page.extract_words()

    # Find case numbers (any year + GS format)
    case_words = [w for w in words if 'GS' in w['text'] and w['x0'] > 100 and w['x0'] < 200 and any(year in w['text'] for year in ['2022', '2023', '2024', '2025'])]

    for case in case_words:
        # Find defendant name words on same row (x0 between 210-360)
        defendant_words = [w for w in words if abs(w['top'] - case['top']) < 1 and 210 < w['x0'] < 360]
        defendant_name = ' '.join([w['text'] for w in sorted(defendant_words, key=lambda x: x['x0'])])

        if defendant_name:
            all_defendants.append({
                'case_number': case['text'].rstrip(','),
                'defendant_name': defendant_name,
                'page': page_num
            })

pdf.close()

print(f'Total defendants found: {len(all_defendants)}')
print(f'\nFirst 10 defendants:')
for d in all_defendants[:10]:
    print(f"  Page {d['page']:2d} | {d['case_number']:20s} | {d['defendant_name']}")

print(f'\nLast 10 defendants:')
for d in all_defendants[-10:]:
    print(f"  Page {d['page']:2d} | {d['case_number']:20s} | {d['defendant_name']}")

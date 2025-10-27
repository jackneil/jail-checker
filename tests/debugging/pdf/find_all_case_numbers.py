import pdfplumber

pdf = pdfplumber.open(r'C:\Github\jail-checker\input\Prosecutor Worklist Report.pdf')

all_case_numbers = []
case_to_defendant = {}

for page_num, page in enumerate(pdf.pages, 1):
    words = page.extract_words()

    # Find ALL words that look like case numbers (contain GS and are in the case number column)
    potential_cases = [
        w for w in words
        if 'GS' in w['text']
        and 100 < w['x0'] < 200
    ]

    for case in potential_cases:
        case_no = case['text'].rstrip(',')
        all_case_numbers.append({
            'case_number': case_no,
            'page': page_num,
            'y_position': case['top']
        })

        # Try to find defendant name on same row
        defendant_words = [
            w for w in words
            if abs(w['top'] - case['top']) < 1
            and 210 < w['x0'] < 360
        ]

        if defendant_words:
            defendant_words_sorted = sorted(defendant_words, key=lambda x: x['x0'])
            defendant_name = ' '.join([w['text'] for w in defendant_words_sorted])
            case_to_defendant[case_no] = {
                'name': defendant_name,
                'page': page_num
            }
        else:
            case_to_defendant[case_no] = {
                'name': None,
                'page': page_num
            }

pdf.close()

print(f'Total case numbers found: {len(all_case_numbers)}')
print(f'Case numbers with defendant names: {sum(1 for v in case_to_defendant.values() if v["name"])}')
print(f'Case numbers WITHOUT defendant names: {sum(1 for v in case_to_defendant.values() if not v["name"])}')

print('\n' + '='*80)
print('CASE NUMBERS WITHOUT DEFENDANT NAMES:')
print('='*80)
for case_no, info in case_to_defendant.items():
    if not info['name']:
        print(f'Page {info["page"]:2d} | {case_no}')

# Also check for any case numbers that don't match our year filter
print('\n' + '='*80)
print('ALL CASE NUMBERS (to verify we got 206):')
print('='*80)
unique_cases = list(dict.fromkeys([c['case_number'] for c in all_case_numbers]))
print(f'Total unique case numbers: {len(unique_cases)}')
for case in unique_cases[:10]:
    print(f'  {case}')
print('  ...')
for case in unique_cases[-10:]:
    print(f'  {case}')

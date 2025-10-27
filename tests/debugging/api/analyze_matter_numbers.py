import pdfplumber
from collections import Counter

pdf = pdfplumber.open(r'C:\Github\jail-checker\input\Prosecutor Worklist Report.pdf')

# Extract all words
all_matter_numbers = []
matter_to_cases = {}

for page_num, page in enumerate(pdf.pages, 1):
    words = page.extract_words()

    # Find matter numbers (left column, contains dash)
    matter_words = [w for w in words if w['x0'] < 100 and '-' in w['text'] and len(w['text']) > 3]

    # Find case numbers on same rows
    for matter_word in matter_words:
        matter_num = matter_word['text']
        all_matter_numbers.append(matter_num)

        # Find case number on same row
        case_words = [w for w in words if 'GS' in w['text'] and 100 < w['x0'] < 200 and abs(w['top'] - matter_word['top']) < 1]

        if case_words:
            case_num = case_words[0]['text'].rstrip(',')
            if matter_num not in matter_to_cases:
                matter_to_cases[matter_num] = []
            matter_to_cases[matter_num].append({
                'case': case_num,
                'page': page_num
            })

pdf.close()

# Count duplicates
counts = Counter(all_matter_numbers)
duplicates = {m: c for m, c in counts.items() if c > 1}

print(f'Total matter number entries: {len(all_matter_numbers)}')
print(f'Unique matter numbers: {len(counts)}')
print(f'Matter numbers appearing more than once: {len(duplicates)}')

print('\n' + '='*80)
print('DUPLICATED MATTER NUMBERS:')
print('='*80)

for matter, count in sorted(duplicates.items(), key=lambda x: -x[1]):
    print(f'\nMatter {matter}: appears {count} times')
    if matter in matter_to_cases:
        for entry in matter_to_cases[matter]:
            print(f'  Page {entry["page"]}: {entry["case"]}')

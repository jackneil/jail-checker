import sys
sys.path.insert(0, r'C:\Github\jail-checker\src')

from parsers import parse_pdf_file

# Parse the PDF
defendants = parse_pdf_file(r'C:\Github\jail-checker\input\Prosecutor Worklist Report.pdf')

print(f'Total defendants: {len(defendants)}')
print(f'\nFirst 10 defendants with matter/case numbers:')
print('='*80)
for d in defendants[:10]:
    print(f'Matter: {d.matter_number:15s} | Case: {d.case_number:20s} | {d.full_name}')

print(f'\n\nChecking for defendants WITHOUT matter numbers:')
no_matter = [d for d in defendants if not d.matter_number]
print(f'Defendants missing matter numbers: {len(no_matter)}')
if no_matter:
    for d in no_matter[:5]:
        print(f'  Case: {d.case_number} | {d.full_name}')

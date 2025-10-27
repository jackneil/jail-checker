"""Test mugshot download and Excel embedding."""

import sys
sys.path.insert(0, r'C:\Github\jail-checker\src')

from io import BytesIO
import requests
from openpyxl import Workbook
from openpyxl.drawing.image import Image

# Test URL from the live custody results
test_url = "https://analytics.southernsoftware.com/crons/CCMugshotsNameID/SC018013C-213349.jpg"

print("Testing mugshot download...")
print(f"URL: {test_url}")
print()

try:
    # Download image
    print("Downloading image...")
    response = requests.get(test_url, timeout=10)
    print(f"Response status: {response.status_code}")
    print(f"Content length: {len(response.content)} bytes")
    print()

    # Create BytesIO and Image object
    print("Creating Image object...")
    image_data = BytesIO(response.content)
    img = Image(image_data)
    img.width = 100
    img.height = 125
    print(f"Image object created: {img}")
    print()

    # Create a workbook and try to add the image
    print("Creating workbook and adding image...")
    wb = Workbook()
    ws = wb.active
    ws.row_dimensions[1].height = 100
    img.anchor = 'A1'
    ws.add_image(img)
    print("Image added to worksheet successfully")
    print()

    # Try to save the workbook
    output_path = r'C:\Github\jail-checker\tests\debugging\test_mugshot.xlsx'
    print(f"Saving workbook to: {output_path}")
    wb.save(output_path)
    print("SUCCESS: Workbook saved successfully!")

except Exception as e:
    print(f"ERROR: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import re

def send_to_google_sheet(data):
    # ✅ Working scopes with Drive access
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)

    # Open the correct spreadsheet and worksheet
    sheet = client.open("ADR E-Commerce 2023").worksheet("RoomData")

    # Get current date - 1
    yesterday = (datetime.today() - timedelta(days=1)).day

    # Get column index by finding the day number in the 3rd row
    header_row = sheet.row_values(3)
    try:
        col_index = header_row.index(str(yesterday)) + 1  # gspread is 1-indexed
    except ValueError:
        print(f"❌ Day {yesterday} not found in row 3 header.")
        return

    # Lookup name column (assumed column A)
    names = sheet.col_values(1)

    updates = 0
    for name, lodging in data:
        # Clean number: "1,234,567" → 1234567
        numeric_value = int(re.sub(r"[^\d]", "", lodging))
        
        # Clean name (remove anything after first comma if exists)
        cleaned_name = name.split(",")[0].strip()

        for i, sheet_name in enumerate(names, start=1):
            if sheet_name.split(",")[0].strip().upper() == cleaned_name.upper():
                sheet.update_cell(i, col_index, numeric_value)
                updates += 1
                break  # only update existing row

    print(f"✅ Updated {updates} rows in column {col_index} (for day {yesterday}).")

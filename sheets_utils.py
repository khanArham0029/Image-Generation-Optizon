from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SHEET_ID = "160H9Eeo4ZBaQHhIfajvLbYC7JUItGK-kX10R5pVvnAU"
RANGE_BASE = "Sheet1!E"  # Column E for image URLs

def get_sheet_data():
    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID, range="Sheet1!A2:D").execute()
    return result.get("values", [])

def write_image_url(row_index, image_url):
    """
    Writes an inline image to Google Sheets using =IMAGE("url") formula.
    This displays the image directly inside the cell.
    """
    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build("sheets", "v4", credentials=creds)

    # Google Sheets formula for displaying image
    image_formula = f'=IMAGE("{image_url}", 1)'  # mode 1 = fit to cell

    range_to_write = f"{RANGE_BASE}{row_index + 2}"  # Row starts from 2 in the sheet
    body = {
        "values": [[image_formula]]
    }

    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        range=range_to_write,
        valueInputOption="USER_ENTERED",  # Required for formula evaluation
        body=body
    ).execute()

if __name__ == "__main__":
    rows = get_sheet_data()
    test_image_url = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-zXrXmZC2HnnA0aPRtDfDKRdM/user-xx7qX6szfoHrUjLX1P1K99L3/img-5gKjpCf0VfL3Rc1sdVOcUUVT.png?st=2025-05-20T11%3A06%3A52Z&se=2025-05-20T13%3A06%3A52Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=cc612491-d948-4d2e-9821-2683df3719f5&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-05-19T16%3A58%3A21Z&ske=2025-05-20T16%3A58%3A21Z&sks=b&skv=2024-08-04&sig=LMfOqdDcH7alvkJ9sY2lE%2BcNu2iV2WwJul/856BIOis%3D"  # Use a real DALL·E 3 URL
    write_image_url(0, test_image_url)  # Writes image to row 2 (0-indexed)

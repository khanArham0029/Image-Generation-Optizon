import os
import mimetypes
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Scope includes Drive access
SCOPES = ['https://www.googleapis.com/auth/drive']
DRIVE_FOLDER_ID = "1YdPku18Iy_bO6t5dHfp8c6-YF8Pxud4T"  

def upload_to_drive(file_path, filename):
    """
    Uploads a file to Google Drive and makes it publicly accessible.
    Returns the public URL for embedding in Google Sheets.
    """
    creds = Credentials.from_service_account_file(
        "credentials.json", scopes=SCOPES
    )
    drive_service = build("drive", "v3", credentials=creds)

    # Prepare file metadata
    file_metadata = {
        "name": filename,
    }
    if DRIVE_FOLDER_ID:
        file_metadata["parents"] = [DRIVE_FOLDER_ID]

    media = MediaFileUpload(
        file_path,
        mimetype=mimetypes.guess_type(file_path)[0]
    )

    # Upload file
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    file_id = file.get("id")

    # Make the file public
    drive_service.permissions().create(
        fileId=file_id,
        body={"role": "reader", "type": "anyone"},
        fields="id"
    ).execute()

    # Return public link
    return f"https://drive.google.com/uc?export=view&id={file_id}"


# for testing 

from PIL import Image

def create_dummy_image(save_path):
    """
    Creates a 256x256 light blue dummy image and saves it to the given path.
    """
    img = Image.new("RGB", (256, 256), color="#ADD8E6")
    img.save(save_path)
    print(f"🖼️ Dummy image saved to {save_path}")

def main():
    filename = "test_drive_upload.png"
    
    # Step 1: Create a dummy image
    create_dummy_image(filename)

    # Step 2: Upload to Google Drive
    try:
        public_url = upload_to_drive(filename, filename)
        print(" Upload successful!")
        print(" Public Image URL:", public_url)
    except Exception as e:
        print(" Upload failed:", e)

if __name__ == "__main__":
    main()
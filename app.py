import streamlit as st
from sheets_utils import get_sheet_data, write_image_url
from image_generator import gpt_generate_dalle_prompt, generate_image_url, download_image

from drive_utils import upload_to_drive
from dotenv import load_dotenv
import os

# Load environment variables (e.g., OPENAI_API_KEY)
load_dotenv()

st.set_page_config(page_title="AI Image Generator", layout="wide")

st.title(" AI Image Generator from Google Sheets")
st.write("This app reads content titles from Google Sheets, generates AI images using OpenAI DALL·E 3, uploads them to Google Drive, and updates the sheet with the embedded image.")

if st.button(" Start Image Generation"):
    with st.spinner("Processing rows... Please wait..."):
        rows = get_sheet_data()

        if not rows:
            st.error("No data found in the Google Sheet.")
        else:
            success_count = 0
            failure_count = 0

            for idx, row in enumerate(rows):
                if len(row) < 4:
                    st.warning(f" Row {idx+2} skipped — missing values.")
                    continue

                title, style, color, theme = row

                try:
                    # Step 1: Generate prompt
                    prompt = gpt_generate_dalle_prompt(title, style, color, theme)
                    st.text(f"[Row {idx+2}] Prompt: {prompt}")

                    # Step 2: Generate image
                    image_url = generate_image_url(prompt)

                    if image_url:
                        # Step 3: Download image locally
                        filename = f"image_{idx+2}.png"
                        if download_image(image_url, filename):
                            
                            # Step 4: Upload to Google Drive
                            public_url = upload_to_drive(filename, filename)

                            # Step 5: Write =IMAGE() formula to sheet
                            write_image_url(idx, public_url)

                            # Step 6: Display in Streamlit
                            st.image(public_url, caption=title, use_column_width=True)

                            # Step 7: Clean up local file
                            os.remove(filename)

                            success_count += 1
                        else:
                            st.error(f"[Row {idx+2}] Image download failed.")
                            failure_count += 1
                    else:
                        st.error(f"[Row {idx+2}] Image generation failed.")
                        failure_count += 1

                except Exception as e:
                    st.error(f"[Row {idx+2}] ❌ Error: {e}")
                    failure_count += 1

            st.success(f" Done! {success_count} images generated and uploaded. {failure_count} rows failed.")

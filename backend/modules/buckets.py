from dotenv import load_dotenv
import os
import requests

load_dotenv()

# Load Supabase credentials from the environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")


def upload_image(file_path):
    # Open the file in binary mode
    print(file_path)
    with open(file_path, "rb") as file:
        # Set the request headers
        headers = {
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/octet-stream",
        }

        # Define the URL for the storage API
        url = f"{
            SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{os.path.basename(file_path)}"

        print(url)

        # Make the PUT request to upload the image
        response = requests.put(url, headers=headers, data=file)

        if response.status_code == 200:
            print("Image uploaded successfully.")
            # Get the public URL for the image
            public_url = f"{
                SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{os.path.basename(file_path)}"
            return public_url
        else:
            print("Error uploading image:", response.json())
            return None

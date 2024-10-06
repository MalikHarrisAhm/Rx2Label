# # import os
# # import requests
# # from dotenv import load_dotenv
# # from data import SERVER_ROOT
# # import json


# # def process_image(img_path):
# #     load_dotenv()
# #     api_key = os.getenv("MISTRAL_API_KEY")

# #     headers = {
# #         "Authorization": "Bearer " + api_key,
# #         "Content-Type": "application/json",
# #     }
# #     print("here")
# #     test = f"{SERVER_ROOT}/{img_path}"
# #     print(test)
# #     res = requests.post(
# #         "https://api.mistral.ai/v1/chat/completions",
# #         headers=headers,
# #         data=json.dumps({
# #             "messages": [
# #                 {
# #                     "role": "user",
# #                     "content": [
# #                         {"type": "text",
# #                             "text": "Can you transcribe the text in the image."},
# #                         {
# #                             "type": "image_url", "image_url": f"{SERVER_ROOT}/{img_path}"
# #                         }
# #                     ]
# #                 }
# #             ]
# #         })
# #     )

# #     data = res.json()
# #     print(data)
# #     print(data['choices'][0]['message']['content'])

# import os
# import requests
# from dotenv import load_dotenv
# import json
# from data import SERVER_ROOT

# # Load environment variables
# load_dotenv()

# # Define the image processing function


# def process_image(img_path):
#     # Get the API key from environment variables
#     api_key = os.getenv("MISTRAL_API_KEY")

#     # Check if the API key was successfully loaded
#     if not api_key:
#         print("API key not found. Please check your environment variables.")
#         return

#     # Define the headers for the API request
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json",
#     }

#     # Construct the image URL using the SERVER_ROOT
#     image_url = f"{SERVER_ROOT}/{img_path}"
#     print("Image URL:", image_url)

#     # Create the payload for the API request
#     payload = {
#         "model": "mistralai/pixtral-12b",  # Ensure correct model for transcription
#         "messages": [
#             {
#                 "type": "text",
#                 "text": "Can you transcribe the text in the image?"
#             },
#             {
#                 "type": "image_url",
#                 "image_url": image_url
#             }
#         ],
#         "max_tokens": 512,
#         "temperature": 0.0
#     }

#     # Send the POST request to the API
#     try:
#         res = requests.post(
#             "https://api.mistral.ai/v1/chat/completions",
#             headers=headers,
#             data=json.dumps(payload)
#         )

#         # Check if the response is successful
#         if res.status_code == 200:
#             # Parse and print the response
#             data = res.json()
#             print(json.dumps(data, indent=4))  # Pretty-print the full response

#             # Extract the transcription result
#             transcription = data['choices'][0]['message']['content']
#             print("Transcription:", transcription)
#         else:
#             # Print an error if the request fails
#             print(f"API request failed with status code {
#                   res.status_code}: {res.text}")
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")


import os
import requests
from dotenv import load_dotenv
import json
from combined import run_check_dosage
from data import SERVER_ROOT

# Load environment variables
load_dotenv()


def process_image(img_path):
    # Get the API key from environment variables
    api_key = os.getenv("MISTRAL_API_KEY")

    if not api_key:
        print("API key not found. Please check your environment variables.")
        return

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "pixtral-12b-2409",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "transcribe this image to text"
                    },
                    {
                        "type": "image_url",
                        "image_url": img_path
                    }
                ]
            }
        ],
        "max_tokens": 1000
    }

    print(img_path)

    try:
        res = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )

        if res.status_code == 200:
            data = res.json()
            transcription = data['choices'][0]['message']['content']

            print(transcription)

            res = run_check_dosage(transcription)
            print(res)
            return res

        else:
            print(
                f"API request failed with status code {
                    res.status_code}: {res.text}"
            )
    except Exception as e:
        print(f"An error occurred: {str(e)}")

import requests
import json
import os
from PyPDF2 import PdfReader
API_KEY = os.getenv("API_KEY", "API_KEY")

def extract_section(file_path, section_title, stop_title, output_file):
    # Load the PDF
    reader = PdfReader(file_path)

    # Extract text from all pages
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()

    # Convert the full text to lowercase for case-insensitive matching
    full_text_lower = full_text.lower()
    section_title_lower = section_title.lower()
    stop_title_lower = stop_title.lower()

    # Find the start and stop positions using `find()`
    start_pos = full_text_lower.find(section_title_lower)
    if start_pos == -1:
        return "Section title not found in document."

    stop_pos = full_text_lower.find(stop_title_lower, start_pos)
    if stop_pos == -1:
        return "Stop title not found in document."

    # Extract the text between start and stop positions
    extracted_text = full_text[start_pos:stop_pos].strip()

    return extracted_text


def find_relevant_dosage_quote(smpc_text):
    # Try to find relevant parts of the SMPC related to dosage
    dosage_keywords = ['dosage', 'dose', '500mg', '750mg', '1g', 'mg', 'recommended dose', 'maximum dose']
    relevant_quotes = []

    # Split the SMPC into sentences for better extraction
    smpc_sentences = smpc_text.split('.')

    # Collect relevant sentences that contain dosage-related keywords
    for sentence in smpc_sentences:
        if any(keyword in sentence.lower() for keyword in dosage_keywords):
            relevant_quotes.append(sentence.strip())

    # Join and return the first few relevant sentences (max 3)
    return ". ".join(relevant_quotes[:3]) + "."


# Define API endpoint and API key (replace with your actual key or use an environment variable)
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("API_KEY", "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")


def check_dosage(prescription_text, smpc_text):
    # Define the conversation with the model
    messages = [
        {
            "role": "user",
            "content": f"""
            Prescription: {prescription_text}

            SMPC Dosage Section: {smpc_text}

            Task: Please check if the prescription dosage is correct according to the SMPC. 
            If there's an error, quote the relevant part of the SMPC snippet that indicates the mistake, 
            and provide the reason for your decision. Output the result in JSON format.
            """
        }
    ]

    # Construct the payload for the API request
    payload = {
        "model": "mistralai/pixtral-12b",  # Ensure the model name is correct for dosage analysis
        "messages": messages,
        "max_tokens": 512,  # Adjust based on response length
        "temperature": 0.0  # Lower temperature for factual correctness
    }

    # Send the request to the Pixtral 12B API
    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            data=json.dumps(payload)
        )

        # Parse and process the response if successful
        if response.status_code == 200:
            result = response.json()
            message_content = result['choices'][0]['message']['content']

            # Clean up the response to remove extra labels like "error_reason" and "relevant_smpc_snippet"
            message_content = message_content.replace('"error_reason":', '').replace('"relevant_smpc_snippet":',
                                                                                     '').strip()

            # Split the response into relevant parts
            lines = message_content.split("\n")
            reason = ""
            smpc_quote = ""

            # Extract the reason and SMPC quote from the response
            for line in lines:
                if "The prescription dosage" in line or "incorrect" in line:
                    reason = line.strip().strip('"')
                elif "The recommended dosage" in line:
                    smpc_quote = line.strip().strip('"')

            # If the API does not provide a valid SMPC quote, extract one manually
            if not smpc_quote or smpc_quote not in smpc_text:
                smpc_quote = find_relevant_dosage_quote(smpc_text)

            return {
                "error": True,
                "reason": reason,
                "smpc_quote": smpc_quote,
                "smpc_quote_valid": True  # The quote is now valid as we manually extracted it
            }

        else:
            # Handle API errors with status code feedback
            return {"error": True, "reason": f"API request failed with status code {response.status_code}.",
                    "smpc_quote": "", "smpc_quote_valid": False}

    except Exception as e:
        # Catch any exceptions during API call
        return {"error": True, "reason": f"Exception occurred: {str(e)}", "smpc_quote": "", "smpc_quote_valid": False}


# Example inputs
file_path = '/Users/malikahmed/Documents/Hack UK/SMPCs/amoxil-article-30-referral-annex-iii_en.pdf'
section_title = 'Posology and method of administration'
stop_title = '4.3 Contraindications'
output_file = 'extracted_section.txt'

smpc_text = extract_section(file_path, section_title, stop_title, output_file)

prescription_text = "Take 2 tablets of Amoxicillin 500mg twice daily for 7 days."

# Check the dosage
result = check_dosage(prescription_text, smpc_text)

# Output the result in pretty JSON format
print(json.dumps(result, indent=4))

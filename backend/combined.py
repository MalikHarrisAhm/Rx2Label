import requests
import json
import os
from PyPDF2 import PdfReader

API_KEY = os.getenv("jVugwoCD6VlA6i6jMuf4azJlxtD0lV0g",
                    "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")
API_URL = "https://openrouter.ai/api/v1/chat/completions"


# Function to extract a section from a PDF
def extract_section(pdf_reader, section_title, stop_title):
    # Load the PDF
    reader = pdf_reader

    # Extract text from all pages
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()

    # Convert the full text to lowercase for case-insensitive matching
    full_text_lower = full_text.lower()
    section_title_lower = section_title.lower()
    stop_title_lower = stop_title.lower()

    # Find the start and stop positions using find()
    start_pos = full_text_lower.find(section_title_lower)
    if start_pos == -1:
        return "Section title not found in document."

    stop_pos = full_text_lower.find(stop_title_lower, start_pos)
    if stop_pos == -1:
        return "Stop title not found in document."

    # Extract the text between start and stop positions
    extracted_text = full_text[start_pos:stop_pos].strip()

    return extracted_text


# Function to find relevant dosage quotes from SMPC text
def find_relevant_dosage_quote(smpc_text):
    dosage_keywords = ['dosage', 'dose', '500mg', '750mg',
                       '1g', 'mg', 'recommended dose', 'maximum dose']
    relevant_quotes = []

    # Split the SMPC into sentences for better extraction
    smpc_sentences = smpc_text.split('.')

    # Collect relevant sentences that contain dosage-related keywords
    for sentence in smpc_sentences:
        if any(keyword in sentence.lower() for keyword in dosage_keywords):
            relevant_quotes.append(sentence.strip())

    # Join and return the first few relevant sentences (max 3)
    return ". ".join(relevant_quotes[:3]) + "."


# Function to check if the prescription dosage is correct according to SMPC
def check_dosage(prescription_text, smpc_text):
    # Define the conversation with the model
    messages = [
        {
            "role": "user",
            "content": f"""
            Prescription: {prescription_text}

            SMPC Dosage Section: {smpc_text}

            Task: Please check if the prescription dosage is correct according to the SMPC.
            Say True if error is detected. Say False if no error.
            If there's an error, quote the relevant part of the SMPC snippet that indicates the mistake,
            and provide the reason for your decision. Output the result in JSON format.
            """
        }
    ]

    # Construct the payload for the API request
    payload = {
        "model": "mistralai/pixtral-12b",
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0.0
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
            error = False
            # Extract the reason and SMPC quote from the response
            for line in lines:
                if "True" in line:
                    error = True
                if "The prescription dosage" in line or "incorrect" in line:
                    reason = line.strip().strip('"')
                elif "The recommended dosage" in line:
                    smpc_quote = line.strip().strip('"')

            # If the API does not provide a valid SMPC quote, extract one manually
            if not smpc_quote or smpc_quote not in smpc_text:
                smpc_quote = find_relevant_dosage_quote(smpc_text)

            return {
                "error": error,
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


# Function to identify the drug based on the prescription text
def identify_drug_from_prescription(prescription_text):
    # Define the conversation with the model
    messages = [
        {
            "role": "user",
            "content": f"""
            Prescription: {prescription_text}

            Task: Please identify the drug this prescription corresponds to from the following options:
            1) Forxiga (dapagliflozin)
            2) Plavix (Clopidogrel)
            3) Xarelto (Rivaroxaban)
            4) Insulin Aspart
            5) Amoxicillin
            6) Pregabalin
            7) Pioglitazone
            8) Duloxetine
            9) Aripiprazole
            10) Febuxostat
            Output only the drug name.
            """
        }
    ]

    # Construct the payload for the API request
    payload = {
        "model": "mistralai/pixtral-12b",
        "messages": messages,
        "max_tokens": 100,
        "temperature": 0.0
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
            drug_name = result['choices'][0]['message']['content'].strip()
            print(drug_name)
            return drug_name
        else:
            return f"API request failed with status code {response.status_code}"

    except Exception as e:
        return f"Exception occurred: {str(e)}"


# Mapping of drug names to their respective file paths from the local directory
drug_pdf_map = {
    "Forxiga": f"{os.getcwd()}/smpcs/forxiga-epar-product-information_en.pdf",
    "Plavix": f"{os.getcwd()}/smpcs/plavix-epar-product-information_en.pdf",
    "Xarelto": f"{os.getcwd()}/smpcs/xarelto-epar-product-information_en.pdf",
    "Insulin Aspart": "smpcs/insulin-aspart-sanofi-epar-product-information_en.pdf",
    "Amoxicillin": f"{os.getcwd()}/smpcs/amoxil-article-30-referral-annex-iii_en.pdf",
    "Pregabalin": f"{os.getcwd()}/smpcs/pregabalin-sandoz-epar-product-information_en.pdf",
    "Pioglitazone": f"{os.getcwd()}/smpcs/pioglitazone-accord-epar-product-information_en.pdf",
    "Duloxetine": f"{os.getcwd()}/smpcs/duloxetine-epar-product-information_en.pdf",
    "Aripiprazole": f"{os.getcwd()}/smpcs/aripiprazole-zentiva-epar-product-information_en.pdf",
    "Febuxostat": f"{os.getcwd()}/smpcs/febuxostat-krka-epar-product-information_en.pdf",
    "Paracetamol": f"{os.getcwd()}/smpcs/SmPC-0003.pdf",
}


def run_check_dosage(prescription_text):

    # Identify the drug from the prescription
    identified_drug = identify_drug_from_prescription(prescription_text)

    if identified_drug in drug_pdf_map:
        file_path = drug_pdf_map[identified_drug]

        # Open the PDF file from the local path
        try:
            with open(file_path, 'rb') as f:
                pdf_reader = PdfReader(f)

                section_title = 'Posology and method of administration'
                stop_title = '4.3 Contraindications'

                # Extract the SMPC text for the identified drug
                smpc_text = extract_section(
                    pdf_reader, section_title, stop_title)

                # Check the dosage
                result = check_dosage(prescription_text, smpc_text)

                # Output the result in pretty JSON format
                print(json.dumps(result, indent=4))

        except Exception as e:
            print(f"Failed to open or process the PDF for {
                identified_drug}: {str(e)}")

    else:
        print(f"Drug {identified_drug} not found in the local PDF map.")

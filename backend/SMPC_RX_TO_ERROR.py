import requests
import json
import os

# Define API endpoint and API key (replace with your actual key or use an environment variable)
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("MISTRAL_API_KEY", "OPENROUTER_API_KEY")


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
            message_content = message_content.replace('"error_reason":', '').replace('"relevant_smpc_snippet":', '').strip()

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

            # Check if the extracted SMPC quote actually exists in the provided SMPC text
            if smpc_quote in smpc_text:
                smpc_quote_valid = True
            else:
                smpc_quote_valid = False
                smpc_quote = "The SMPC quote provided does not exist in the original SMPC text."

            return {
                "error": True,
                "reason": reason,
                "smpc_quote": smpc_quote,
                "smpc_quote_valid": smpc_quote_valid  # Boolean to indicate if the quote is valid or hallucinated
            }

        else:
            # Handle API errors with status code feedback
            return {"error": True, "reason": f"API request failed with status code {response.status_code}.", "smpc_quote": "", "smpc_quote_valid": False}

    except Exception as e:
        # Catch any exceptions during API call
        return {"error": True, "reason": f"Exception occurred: {str(e)}", "smpc_quote": "", "smpc_quote_valid": False}

# Example inputs
prescription_text = "Take 2 tablets of Amoxicillin 500mg twice daily for 7 days."
smpc_text = "The recommended dosage of Amoxicillin is 500mg three times a day for adults with moderate infections."

# Check the dosage
result = check_dosage(prescription_text, smpc_text)

print("Prescription Text:", prescription_text)
print("SmPC Text:", smpc_text)
# Output the result in pretty JSON format
print(json.dumps(result, indent=4))

from PyPDF2 import PdfReader

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

    # Save the extracted section to a .txt file
    with open(output_file, 'w') as file:
        file.write(extracted_text)

    return f"Section saved to {output_file}"

# Example usage
file_path = '/path/to/xarelto-epar-product-information_en.pdf'
section_title = 'Posology and method of administration'
stop_title = '4.3 Contraindications'
output_file = 'extracted_section.txt'

result = extract_section(file_path, section_title, stop_title, output_file)

# Output result message
print(result)

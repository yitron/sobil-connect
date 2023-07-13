import streamlit as st
from pdf_parser import PDFParser
from error_handler import ErrorHandler
import json

def main():
    st.title("Bank Statement Parser")

    # Create instances of PDFParser and ErrorHandler
    parser = PDFParser()
    error_handler = ErrorHandler()

    # File upload section
    st.subheader("Upload PDF File")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file:
        try:
            # Extract text from uploaded PDF file
            extracted_text = parser.extract_text_from_pdf(uploaded_file)

            # Parse extracted text to JSON format
            parsed_json = parser.parse_to_json(extracted_text)
            print(extracted_text)  # Verify the parsed JSON data

            # Save JSON file locally
            json_file_name = "parsed_bank_statement.json"
            with open(json_file_name, "w") as json_file:
                json.dump(parsed_json, json_file, indent=4)  # Use 'indent' parameter for pretty formatting

            st.success("PDF file parsed and JSON file saved successfully.")
            st.download_button("Download JSON", data=json_file_name, file_name=json_file_name)
        except Exception as e:
            error_message = f"Error occurred during PDF parsing: {str(e)}"
            error_handler.log_error(error_message)
            st.error("An error occurred during PDF parsing. Please try again.")

if __name__ == "__main__":
    main()

import pytesseract
from PyPDF2 import PdfReader
import json
import re
import tempfile
import os

class PDFParser:
    def __init__(self):
        pass

    def extract_text_from_pdf(self, pdf_file):
        # Save the uploaded PDF file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(pdf_file.read())
            temp_file_path = temp_file.name

        # Use PyPDF2 to extract text from the PDF file
        with open(temp_file_path, "rb") as file:
            pdf = PdfReader(file)
            extracted_text = ""
            for page in pdf.pages:
                extracted_text += page.extract_text()

        # Delete the temporary file
        if temp_file_path:
            os.remove(temp_file_path)

        return extracted_text

    def parse_to_json(self, extracted_text):
        # Parse extracted text to JSON format
        parsed_json = {}

        # Parse the overview section
        overview_pattern = r"\"overview\": \{\s+\"bank_name\": \"(.*?)\",\s+\"account_name\": \"(.*?)\",\s+\"account_number\": \"(.*?)\",\s+\"currency\": \"(.*?)\",\s+\"printed_by\": \"(.*?)\",\s+\"printed_on\": \"(.*?)\",\s+\"opening_balance\": ([0-9,.]+),\s+\"available_balance\": ([0-9,.]+)\s+}"
        overview_match = re.search(overview_pattern, extracted_text, re.DOTALL)
        if overview_match:
            parsed_json["overview"] = {
                "bank_name": overview_match.group(1),
                "account_name": overview_match.group(2),
                "account_number": overview_match.group(3),
                "currency": overview_match.group(4),
                "printed_by": overview_match.group(5),
                "printed_on": overview_match.group(6),
                "opening_balance": float(overview_match.group(7).replace(",", "")),
                "available_balance": float(overview_match.group(8).replace(",", ""))
            }

        # Parse the transactions section
        transactions_pattern = r"\"transacQons\": \[([^]]+)\]"
        transactions_match = re.search(transactions_pattern, extracted_text)
        if transactions_match:
            transactions_data = transactions_match.group(1)
            transactions_list = re.findall(r"\{([^}]+)\}", transactions_data)
            parsed_json["transactions"] = []
            for transaction_data in transactions_list:
                transaction_match = re.search(r"\"date\": \"(.*?)\",\s+\"type\": \"(.*?)\",\s+\"amount\": ([0-9,.]+),\s+\"descripQon\": \"(.*?)\"", transaction_data)
                if transaction_match:
                    transaction = {
                        "date": transaction_match.group(1),
                        "type": transaction_match.group(2),
                        "amount": float(transaction_match.group(3).replace(",", "")),
                        "description": transaction_match.group(4)
                    }
                    parsed_json["transactions"].append(transaction)

        return parsed_json
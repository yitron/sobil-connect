import unittest
from pdf_parser import PDFParser

class TestPDFParser(unittest.TestCase):
    def setUp(self):
        self.parser = PDFParser()

    def test_extract_text_from_pdf(self):
        # Test extracting text from a sample PDF file
        with open("sample.pdf", "rb") as file:
            expected_text = file.read().decode("utf-8")
        extracted_text = self.parser.extract_text_from_pdf(file)
        self.assertEqual(extracted_text, expected_text)

    def test_parse_to_json(self):
        # Test parsing extracted text to JSON format
        expected_json = {
            "overview": {
                "bank_name": "DBS Bank Limited",
                "account_name": "A Small Business Pte. Ltd.",
                "account_number": "75834726",
                "currency": "SGD",
                "printed_by": "Tan Ah Kow",
                "printed_on": "July 2023",
                "opening_balance": 150000.0,
                "available_balance": 120345.0
            },
            "transactions": [
                {
                    "date": "2023-07-01",
                    "type": "credit",
                    "amount": 5000.0,
                    "description": "Sale of goods - Invoice #INV1234"
                },
                {
                    "date": "2023-07-02",
                    "type": "debit",
                    "amount": 1500.0,
                    "description": "Office supplies - Purchase from OfficeMart"
                },
                # Add more expected transactions
            ]
        }
        extracted_text = '''{"overview": {"bank_name": "DBS Bank Limited", "account_name": "A Small Business Pte. Ltd.", "account_number": "75834726", "currency": "SGD", "printed_by": "Tan Ah Kow", "printed_on": "July 2023", "opening_balance": 150000.0, "available_balance": 120345.0}, "transacQons": [{"date": "2023-07-01", "type": "credit", "amount": 5000.0, "descripQon": "Sale of goods - Invoice #INV1234"}, {"date": "2023-07-02", "type": "debit", "amount": 1500.0, "descripQon": "Office supplies - Purchase from OfficeMart"}]}'''
        parsed_json = self.parser.parse_to_json(extracted_text)
        self.assertEqual(parsed_json, expected_json)

if __name__ == '__main__':
    unittest.main()

import logging

class ErrorHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)
        self.file_handler = logging.FileHandler('error.log')
        self.file_handler.setLevel(logging.ERROR)
        self.file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(self.file_handler)

    def log_error(self, error_message):
        self.logger.error(error_message)

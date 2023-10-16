import sys
from sensor.logger import logging

class SensorException(Exception):

    def __init__(self, error_message, error_detail:sys):
        super().__init__()
        self.error_message = SensorException.prepare_error_message(error_message, error_detail)

    @staticmethod
    def prepare_error_message(error_message, error_detail:sys)->str:

        _, _, exc_tb = error_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_no = exc_tb.tb_lineno
        error_message = f"Error occured in script name [{file_name}] on line no. [{line_no}], error message: [{error_message}]"
        logging.info(error_message)

        return error_message
    
    def __repr__(self) -> str:
        return self.error_message
    
    def __str__(self) -> str:
        return self.error_message
import sys
import os
from src import logger

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message= self.get_detail_error_message(error_message=error_message, error_detail=error_detail)

    @staticmethod
    def get_detail_error_message(error_message, error_detail:sys):

        _,_, exc_tb= error_detail.exc_info()
        file_name= exc_tb.tb_frame.f_code.co_filename
        line_no= exc_tb.tb_lineno
        error_message_detail= f"Error occurred in {file_name}, line{line_no}: {str(error_message)}"

        return error_message_detail
    
    def __str__(self):
        return self.error_message

import os 
import sys


def error_deatails(error,error_detail: sys):
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    errormessage="Error occured in the filename [{0}] line number [{1}] error message [{2}]".format(file_name,exc_tb,str(error))

    return errormessage


class CustomException(Exception):
    def __init__(self,errormessage,error_detail):
        super().__init__(errormessage)
        self.errormessage=error_deatails(errormessage,error_detail=error_detail)
    
    def __str__(self):
        return self.errormessage

from Hatetext.logger import logging
from Hatetext.exception import CustomException
import sys 

#logging.info("welcome to my projectsssss")

try:
    a=6/"0"

except Exception as e:
    raise CustomException(e,sys) from e
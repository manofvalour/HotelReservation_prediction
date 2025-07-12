import logging
import os ##for creating directory
from datetime import datetime

LOGFILE= f"{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.log" ## logging file name
log_dir = os.path.join(os.getcwd(), "logs", LOGFILE) ## file directory
os.makedirs(log_dir, exist_ok=True)

log_name= os.path.join(log_dir, LOGFILE)

logging.basicConfig(
    filename=log_name,
    format= "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def get_logger(name):
    logger= logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
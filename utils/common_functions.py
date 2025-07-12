import os
import pandas as pd
from src.logger import get_logger
from src.exception import CustomException
import yaml
import sys
from config.path_config import *

logger = get_logger(__name__)

##creating function to read yaml file
def read_yaml(file_path):
    """
    This function reads yaml files. It takes file_path as the required parameter.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError (f"File is not in the given path")
        
        else:
            with open(file_path, 'r') as yaml_file:
                config = yaml.safe_load(yaml_file)
                logger.info("successfully read the yaml file")
        return config
        
    except Exception as e:
        logger.error('Error while reading YAML file')
        raise CustomException('failed to read yaml file', sys)


## function for loading data
def load_data(file_path):
    try:
        logger.info("Loading data")
        return pd.read_csv(file_path)

    except Exception as e:
        logger.error(f"Error loading the data{e}")
        raise CustomException("Failed to load data", sys)
    
## function for saving data to pkl or csv format
def save_data(data, file_path, file_name):
    #file_name== '%.pkl':
    return data.to_pickle(file_path)
    #else:
    #return data.to_csv(file_path)
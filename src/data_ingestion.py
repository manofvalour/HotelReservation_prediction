import os ##for path manipulation
import pandas as pd ## for data handling
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.exception import CustomException
from src.logger import get_logger
from config.path_config import *
from utils.common_functions import read_yaml
import sys

##initializing logger
logger=get_logger(__name__)

## Creating a DataIngestion class
class DataIngestion:
    def __init__(self,config):
        self.config=config['data_ingestion']
        self.bucket_name= self.config['bucket_name']
        self.bucket_file_name = self.config['bucket_file_name']
        self.train_test_split = self.config['test_ratio']
        self.random_state = self.config['random_state']

        os.makedirs(RAW_DATA_DIR, exist_ok=True)
        os.makedirs(PROCESSED_DATA_DIR, exist_ok=True )

        logger.info(f'Data Ingestion started with {self.bucket_name} and file name is {self.bucket_file_name}')

    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)

            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f'CSV file is successfully downloaded to {RAW_FILE_PATH}')

        except Exception as e:
            logger.error("Error while downloading csv file")
            raise CustomException("failed to download csv file", sys)
        
    def download_csv_from_local_file_path(self):
        try:
            ##reading the dataset
            data= pd.read_csv(DATA_FILE_PATH)

            ##saving the dataset to Data file path
            data.to_csv(RAW_FILE_PATH)

            logger.info(f'Data successfully downloaded to {RAW_FILE_PATH}')
        
        except Exception as e:
            logger.error("Error while downloading csv dataset")
            raise CustomException("failed to download csv dataset", sys)

        
    def split_data(self):
        try:
            logger.info("starting the splitting process")

            ## importing the data and converting to DataFrame
            data = pd.read_csv(RAW_FILE_PATH)

            ## splitting the raw dataset into train and test data
            train_data, test_data=train_test_split(data, test_size=self.train_test_split, 
                                                   random_state=self.random_state)
            
            ## saving the dataset
            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)
            
            logger.info(f'Train data saved to {TRAIN_FILE_PATH}')
            logger.info(f"Test data saved to {TEST_FILE_PATH}")

        except Exception as e:
            logger.error('Error while splitting and saving the data split')
            raise CustomException("failed to split data into training and test sets", sys)
        
    def run(self):
        try:
            logger.info('Starting data ingestion process')
            self.download_csv_from_local_file_path()
            self.split_data()

        except CustomException as ce:
            logger.error(f"CustomException: {ce}")
            raise CustomException(ce, sys)

        finally:
            logger.info("Data Ingestion Completed Successfully")

        
    #if __name__== "__main__":
     #   config= read_yaml(CONFIG_PATH)
      #  data_ingestion= DataIngestion(config)
       # data_ingestion.run()
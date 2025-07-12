import os

################### DATA INGESTION PATH #############################
RAW_DATA_DIR = 'artifact/data/raw'
PROCESSED_DATA_DIR = 'artifact/data/pre_processed'

RAW_FILE_PATH = os.path.join(RAW_DATA_DIR, 'raw.csv')
TRAIN_FILE_PATH = os.path.join(PROCESSED_DATA_DIR, 'train.csv')
TEST_FILE_PATH = os.path.join(PROCESSED_DATA_DIR, 'test.csv')

CONFIG_PATH = "config/config.yaml"

DATA_FILE_PATH= "Hotel_Reservations/Hotel_Reservations.csv"



################### DATA PROCESSING ##################################
PROCESSED_DIR = 'artifact/processed'

PROCESSED_TRAIN_DATA_PATH =os.path.join(PROCESSED_DIR, "processed_train.csv")
PROCESSED_TEST_DATA_PATH =os.path.join(PROCESSED_DIR, "processed_test.csv")

################# MODEL TRAINING ######################################
MODEL_PATH = 'artifact/models/rf_model.pkl'
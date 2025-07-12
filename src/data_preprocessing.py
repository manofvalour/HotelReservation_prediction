import os
import sys
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.exception import CustomException
from config.path_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)


class DataProcessor:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path= train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)

        ##creating the processed directory
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def preprocess_data(self, df):
        try:
            logger.info('Starting our Data Processing Step')

            logger.info('dropping unnecessary and duplicated columns')
            df.drop(columns=["Unnamed: 0.1", "Unnamed: 0", "Booking_ID"], inplace=True)
            df.drop_duplicates(inplace=True)

            logger.info("splitting categorical and numerical columns")
            #cat_cols= [column for column in df.columns if df[column].dtypes == 'O']
            #num_cols = [column for column in df.columns if df[column].dtypes !='O']
            cat_cols = self.config["data_processing"]['categorical_columns']
            num_cols = self.config['data_processing']['numerical_columns']

            logger.info('Applying label Encoding')
            label_encoder=LabelEncoder()
            mappings ={}

            for col in cat_cols:
                df[col]= label_encoder.fit_transform(df[col])

                mappings[col] = {label:code for label, code in zip(label_encoder.classes_, 
                                                                   label_encoder.transform
                                                                   (label_encoder.classes_))}
            logger.info('Label Mappings are :')
            for col, mapping in mappings.items():
                    logger.info(f"{col}: {mapping}")

            logger.info("Doing skewness handling")
            skewness_threshold= self.config['data_processing']['skewness_threshold']
            skewness=df[num_cols].apply(lambda x:x.skew())
            
            ##applying log transformation
            for column in skewness[skewness>skewness_threshold].index:
                df[column]= np.log1p(df[column])

            return df

        except Exception as e:
            logger.error(f"Error during preprocess step {e}")
            raise CustomException('Error while preprocess data', e)
        
    def balanced_data(self, df):
        try:
            logger.info("Handling Imbalanced Data")
            
            X =df.drop(columns=['booking_status'])
            y= df['booking_status']

            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X,y)

            balanced_df= pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df['booking_status']=y_resampled

            logger.info('Data Balanced Successfully')

            return balanced_df
        
        except Exception as e:
            logger.error(f"Error while preprocessing imbalanced data {e}")
            raise CustomException('Error while processing imbalanced data', e)
    
    def feature_selection(self, df):
        try:
            logger.info("Starting feature selection step")

            #splitting X and y
            X =df.drop(columns=['booking_status'])
            y= df['booking_status']

            ## Training random forest model for feature importance
            model= RandomForestClassifier(random_state=42)
            model.fit(X,y)

            feature_importance = model.feature_importances_

            feature_importance_df = pd.DataFrame({'feature': X.columns,
                                                  'importance': feature_importance})
            
            top_num_features_df= feature_importance_df.sort_values(by= 'importance', ascending=False)

            ## selecting the top10 most relevant features
            num_features_to_select = self.config['data_processing']['no_of_features']
            top_features_to_select = top_num_features_df['feature'].head(num_features_to_select).values
            
            logger.info(f"Features selected: {top_features_to_select}")
            top_features_df = df[top_features_to_select.tolist() + ['booking_status']]

            logger.info('features selection completed')
            return top_features_df
        
        except Exception as e:
            logger.error(f'Error during feature selection process {e}')
            raise CustomException("Error during feature selection process", e)
        
    def save_data(self, df, file_path):
        try:
            logger.info('Saving our data in procesed directory')
            df.to_csv(file_path, index=False)

            logger.info(f"Data saved successfully to {file_path}")
        except Exception as e:
            logger.error(f"Error while saving data to {file_path}")
            raise CustomException("Error while saving data", e)
        
    def process(self):
        try:
            logger.info("Loading the data from Raw directory")

            train_df= load_data(self.train_path)
            test_df = load_data(self.test_path)
            
            train_df= self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balanced_data(train_df)
            test_df = self.balanced_data(test_df)

            train_df = self.feature_selection(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)

            logger.info("Data Processing completed successfully")
        
        except Exception as e:
            logger.error(f"error during data preprocessing pipeine")
            raise CustomException(e, sys)        

#    if __name__== "__main__":
 #       preprocessor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
 #       preprocessor.process()
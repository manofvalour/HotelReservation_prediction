import pandas
import numpy
import os
import sys

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
from scipy.stats import randint
#import mlflow
#import mlflow.sklearn


from src.logger import get_logger
from src.exception import CustomException
from config.model_params import *
from config.path_config import *
from utils.common_functions import read_yaml, load_data

logger = get_logger(__name__) ## initializing the logging class

## creating class for model training

class ModelTraining():
    def __init__(self, train_path, test_path, model_output_path):
        self.train_path= train_path
        self.test_path= test_path
        self.model_output_path = model_output_path

        self.params_dist= RF_PARAMS ## random forest models parameter
        self.random_search_params = RANDOM_SEARCH_PARAMS ## parameters for hyperparameter tuning

    def load_and_split_data(self):
        try:
            logger.info(f'loading train data from {self.train_path}')
            train_df= load_data(self.train_path)

            logger.info(f'loading test data from {self.test_path}')
            test_df= load_data(self.test_path)

            X_train = train_df.drop(columns=['booking_status'])
            y_train = train_df['booking_status']

            X_test = test_df.drop(columns=['booking_status'])
            y_test = test_df['booking_status']

            logger.info ('Data loaded and splitted successfully for model training')

            return X_train, y_train, X_test, y_test

        except Exception as e:
            logger.error(f"error while loading data {e}")
            raise CustomException('failed to load data', sys)
    

    def train_model(self, X_train, y_train):
        try:
            logger.info('Initializing our model')

            rf_model = RandomForestClassifier(random_state=self.random_search_params['random_state'])

            logger.info("Starting our hyperparamete tuning")

            random_search = RandomizedSearchCV(estimator=rf_model, 
                                           param_distributions=self.params_dist,
                                           n_iter=self.random_search_params['n_iter'],
                                           cv= self.random_search_params['cv'],
                                           n_jobs= self.random_search_params['n_jobs'],
                                           verbose= self.random_search_params['verbose'],
                                           random_state=self.random_search_params['random_state'],
                                           scoring=self.random_search_params['scoring']
                                           )
        
            logger.info("starting our hyperparameter tuning")

            random_search.fit(X_train, y_train)

            logger.info('Hyperparameter tuning completed')

            best_params=random_search.best_params_
            best_rf_model= random_search.best_estimator_

            logger.info(f"Best parameters are : {best_params}")

            return best_rf_model

        except Exception as e:
            logger.error(f"Error while training model {e}")
            raise CustomException('failed to train model', sys)
    

    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info('Evaluating our model')
            y_pred = model.predict(X_test)

            accuracy= accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1= f1_score(y_test, y_pred)

            logger.info(f"Accuracy_score: {accuracy}")
            logger.info(f"Precision score: {precision}")
            logger.info(f"Recall_score: {recall}")
            logger.info(f"f1_score: {f1}")

            return {
                'accuracy': accuracy,
                'precison': precision,
                'recall' : recall,
                'f1_score': f1
            }
    
        except Exception as e:
            logger.info('Error while evaluating model')
            raise CustomException('Failed to evaluate model', sys)
    
    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)

            logger.info('Saving the model')
            joblib.dump(model, self.model_output_path)
        
            logger.info(f'model saved to {self.model_output_path}')

    
        except Exception as e:
            logger.info("Error while saving the model")
            raise CustomException(e, sys)
    
    def run(self):
        
        #with mlflow.start_run():

            try:
                logger.info('Starting model training pipeline')
                logger.info('starting our mlflow Experimentation')

               # logger.info('logging the training and testing dataset into MLFLOW')
              #  mlflow.log_artifact(self.train_path, artifact_path ='datasets')
               # mlflow.log_artifact(self.test_path, artifact_path = 'datasets')

                X_train, y_train, X_test, y_test= self.load_and_split_data()
                best_rf_model= self.train_model(X_train, y_train)
                metrics=self.evaluate_model(best_rf_model, X_test, y_test)
                self.save_model(best_rf_model)

                #logger.info('logging the model into MLFLOW')
                #mlflow.log_artifact(self.model_output_path)

                #logger.inof('logginf the parameters and metrics to MLFLOW')
                #mlflow.log_params(best_rf_model.get_params())
                #mlflow.log_metrics(metrics)

                logger.info("Model Training successfully Completed")

            except Exception as e:
                logger.info("Error occured while runing model training pipeline")
                raise CustomException (e, sys)
            

  #  if __name__=='__main__':
    #    modeltraining=ModelTraining(PROCESSED_TRAIN_DATA_PATH,
   #                                 PROCESSED_TEST_DATA_PATH,
    #                                MODEL_PATH)
        
  #      modeltraining.run()
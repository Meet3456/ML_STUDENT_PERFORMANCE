import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

## Dataclass -> python decorator to create class, that are mainly used to store data
## It automatically generates special methods like __init__ and __repr__ for you.
@dataclass
class DataIngestionConfig:
    ## Providing the path to store the TrainingData.csv under new folder 'Artifacts' -> str: Default value:
    train_data_path: str = os.path.join('artifacts',"train.csv")
    ## Providing the path to store the TestData.csv
    test_data_path: str = os.path.join('artifacts',"test.csv")
    ## Providing the path to store the RawData.csv
    raw_data_path: str = os.path.join('artifacts',"data.csv")   

class DataIngestion:
    ## The `__init__` method of this class initializes the `ingestion_config` attribute to a `DataIngestionConfig` object. Now ingestion_config can access all the variables (i.e train,test and raw datapath) of class DataIngestionConfig
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            ## Reading the data:
            df=pd.read_csv('notebooks/data/StudentsPerformance.csv')
            logging.info('Read the dataset as dataframe')            

            ## This line creates a directory structure specified by the train_data_path if it doesn't already exist. It uses the os.makedirs function and sets exist_ok to True to avoid errors if the directory already exists.
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            ## This line saves the DataFrame df as a CSV file at the path specified by raw_data_path, without including the index and with column headers.
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            ## Converting the training data to csv and storing in the respective location:
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            ## Converting the test data to csv and storing in the respective location:
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            logging.info("Data ingestion completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path

            )
        except Exception as e:
            raise CustomException(e,sys)

## Drivers Code to initialize Data Ingestion:        
if __name__=="__main__":
    ## Creating an object of class:
    obj=DataIngestion()
    ## Returns 2 values:the path to train and test data ans storing it:
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr,test_arr,_ = data_transformation.initiate_data_transformation(train_path=train_data,test_path=test_data)

    ## initiate_data_transformation returns three value train_arr,test_arr and the path of preprocessor object where it is created and takes 2 inputt the train_path and the test_path
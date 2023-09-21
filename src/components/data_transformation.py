import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")
    # Providing  the path for preprocessor object(used for Transformation of Numerical and Categorical Columns:in Artifacts folder as pkl file:)

class DataTransformation:
    def __init__(self):
        ## data_transformation_config can access preprocess_obj_file_path:
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This function is responsible for data trnasformation and returning the preprocessor object -> That performs Transformation on Numerical and Categorical Columns:        
        '''
        try:
            numerical_columns = ["reading score", "writing score"]
            categorical_columns = [
                "gender",
                "race/ethnicity",
                "parental level of education",
                "lunch",
                "test preparation course",
            ]
            # For Numerical columns:
            num_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())

                ]
            )
            # For Categorical Cloumns:
            cat_pipeline=Pipeline(

                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
                ]

            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")
            # Combining two pipelines Using Column Transformer:
            preprocessor=ColumnTransformer(
                [
                ## Applying numerical pipeline on numerical columns
                ("num_pipeline",num_pipeline,numerical_columns),
                ## Applying categorical pipeline on categorical columns
                ("cat_pipelines",cat_pipeline,categorical_columns)

                ]
            )

            # Returning the object:That Transforms the data(ohe and scaling data)
            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        

    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed,from train and test path:")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()
            ## As the above fumction returns preprocessor storing it in preprocessing_obj

            ## The column which is to be predicted
            target_column_name="math score"
            numerical_columns = ["writing score", "reading score"]

            # Splitting the Train-df into input and output fetaures df:
            # Except the target columns all are the input Features:
            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            # Splitting the Test-df into input and output fetaures df:
            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            ## fit_transform of preprocessor object on Independent features(input_features)of Train DataFrame:    
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            ## transform of preprocessor object on Independent features(input_features)of Test DataFrame:  
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            ## Target feature ko preprocess nahi kar sakte:!!


            ## The final Training array Dataset -> consisting of preprocessed input features of train_df and target feature of train_df(converted to array)-> np.array
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            logging.info(f"Saved preprocessing object.")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj,
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
    
        except Exception as e:
            raise CustomException(e,sys)
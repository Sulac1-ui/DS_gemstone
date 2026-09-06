import os 
import sys

from dataclasses import dataclass

from src.exceptions import CustomException
from src.logger import logging

import pandas as pd 
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder,StandardScaler


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file = os.path.join('artifact', 'preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.DataTransformation_config= DataTransformationConfig()

    def get_data_transformation(self):
        '''
        This function is responsible for Data Transformation.
        '''

        try:
            # Define which columns should be ordinal-encoded and which should be scaled
            categorical_cols = ['cut', 'color','clarity']
            numerical_cols = ['carat', 'depth','table', 'x', 'y', 'z']
            # Define the custom ranking for each ordinal variable
            cut_categories = ['Fair', 'Good', 'Very Good','Premium','Ideal']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']

            numerical_pipeline= Pipeline(
                steps= [
                    ("imputer", SimpleImputer(strategy= 'median')),
                    ("scale", StandardScaler())
                    ]
                )

            # Categorical Pipeline
            cat_pipeline = Pipeline(
                            steps=[
                            ('imputer',SimpleImputer(strategy='most_frequent')),
                            ('ord-encoder',OrdinalEncoder(categories=[cut_categories,color_categories,clarity_categories])),
                            ('scaler',StandardScaler())
                            ]
                        )
            logging.info(f'Categorical Columns"{categorical_cols}')
            logging.info(f'Numerical Columns   : {numerical_cols}')


            preprocessor= ColumnTransformer(
                [
                    ("num_pipeline", numerical_pipeline, numerical_cols),
                    ("cat_pipeline", cat_pipeline, categorical_cols)
                ]
            )
            return preprocessor
        
        except Exception as e:
            logging.info('Exception occured in Data Transformation Phase')
            raise Exception(e, sys)


    
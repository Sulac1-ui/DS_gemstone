import os 
import sys

from src.exceptions import CustomException
from src.logger import logging

import pandas as pd
from sklearn.model_selection import train_test_split

from dataclasses import dataclass

from src.Components.Data_transformation import DataTransformationConfig, DataTransformation
from src.Components.Model_trainer import ModelTrainer  # Matches the imported class name

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifact', 'train.csv')
    test_data_path: str = os.path.join('artifact', 'test.csv')
    raw_data_path: str = os.path.join('artifact', 'data.csv')

class Dataingestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            logging.info("Started Data Ingestion method")
            df = pd.read_csv("/Users/Admin/Me only/DS project/Notebook/Data/gemstone.csv")
            logging.info('Dataset read as pandas Dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False)

            logging.info("Train and Test Split Initiating")

            train_set, test_set = train_test_split(df, random_state=42, test_size=0.2)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Training and Testing Data Saved Successfully!")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            # Fixed to raise CustomException properly
            raise CustomException(e, sys)


if __name__ == '__main__':
    obj = Dataingestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)

    # Fixed: Use the exact class name imported from Model_trainer.py
    model_trainer_obj = ModelTrainer()
    model_trainer_obj.initiate_model_training(train_arr, test_arr)
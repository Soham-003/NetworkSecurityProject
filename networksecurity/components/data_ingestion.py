import os
import sys
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from dotenv import load_dotenv
from pymongo import MongoClient

from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.data_transformation import DataTransformationConfig

from networksecurity.components.model_trainer import ModelTrainerConfig
from networksecurity.components.model_trainer import ModelTrainer

# Load environment variables
load_dotenv()

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "raw_data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            # ✅ Step 1: Connect to MongoDB
            mongo_uri = os.getenv("MONGO_DB_URL")   # stored in .env
            if not mongo_uri:
                raise ValueError("MongoDB URI not found in .env file")

            client = MongoClient(mongo_uri)
            logging.info("Connected to MongoDB successfully")

            # ✅ Step 2: Fetch data from MongoDB
            db = client["WebsitePhishingData"]               # <-- replace with your DB name
            collection = db["NetworkData"]               # <-- replace with your collection name

            data = list(collection.find({}, {"_id": 0}))  # exclude MongoDB default _id
            df = pd.DataFrame(data)
            logging.info(f"Fetched {df.shape[0]} records from MongoDB")

            # ✅ Step 3: Save raw data
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            # ✅ Step 4: Train-test split
            logging.info("Train-test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42, stratify=df['Result'])

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))

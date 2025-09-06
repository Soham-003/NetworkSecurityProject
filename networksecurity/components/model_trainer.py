import os
import sys
from dataclasses import dataclass

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.utils.utils import save_object


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            # Use a single best model
            logging.info("Training Gradient Boosting Classifier")
            model = LogisticRegression()
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            logging.info(f"Model Accuracy: {accuracy:.4f}")

            if accuracy < 0.6:
                raise CustomException("Model accuracy is less than 0.6. Not acceptable.")

            # Save the trained model
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=model,
            )

            return accuracy

        except Exception as e:
            raise CustomException(e, sys)

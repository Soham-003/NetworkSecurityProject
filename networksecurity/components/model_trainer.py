import os
import sys
from dataclasses import dataclass

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
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
            model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            logging.info(f"Model Accuracy: {accuracy:.4f}")
            logging.info(f"Classification Report:\n{classification_report(y_test, y_pred)}")
            logging.info(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")

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

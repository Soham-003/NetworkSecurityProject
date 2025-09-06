import sys
import pandas as pd
import os
from networksecurity.exception.exception import CustomException
from networksecurity.utils.utils import load_object


import pandas as pd

class CustomData:
    def __init__(self, 
                 SFH:int, 
                 popUpWidnow:int, 
                 SSLfinal_State:int, 
                 Request_URL:int, 
                 URL_of_Anchor:int, 
                 web_traffic:int, 
                 URL_Length:int, 
                 age_of_domain:int, 
                 having_IP_Address:int):
        
        self.SFH = SFH
        self.popUpWidnow = popUpWidnow
        self.SSLfinal_State = SSLfinal_State
        self.Request_URL = Request_URL
        self.URL_of_Anchor = URL_of_Anchor
        self.web_traffic = web_traffic
        self.URL_Length = URL_Length
        self.age_of_domain = age_of_domain
        self.having_IP_Address = having_IP_Address

    def get_data_as_data_frame(self):
        try:
            data_dict = {
                "SFH": [self.SFH],
                "popUpWidnow": [self.popUpWidnow],
                "SSLfinal_State": [self.SSLfinal_State],
                "Request_URL": [self.Request_URL],
                "URL_of_Anchor": [self.URL_of_Anchor],
                "web_traffic": [self.web_traffic],
                "URL_Length": [self.URL_Length],
                "age_of_domain": [self.age_of_domain],
                "having_IP_Address": [self.having_IP_Address]
            }
            return pd.DataFrame(data_dict)
        except Exception as e:
            raise e
import sys
import os
import pandas as pd
import pickle

class PredictPipeline:
    def __init__(self):
        # Load saved model and preprocessor
        model_path = os.path.join("artifacts","model.pkl")
        preprocessor_path = os.path.join("artifacts","preprocessor.pkl")
        
        with open(model_path,"rb") as f:
            self.model = pickle.load(f)
        with open(preprocessor_path,"rb") as f:
            self.preprocessor = pickle.load(f)

    def predict(self, features: pd.DataFrame):
        try:
            data_scaled = self.preprocessor.transform(features)
            preds = self.model.predict(data_scaled)
            return preds
        except Exception as e:
            raise e


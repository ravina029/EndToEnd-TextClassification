import sys
import os 
import io
import keras 
import pickle 
from PIL import Image
from Hatetext.logger import logging
from Hatetext.constant import *
from Hatetext.exception import CustomException
from keras.utils import pad_sequences
from Hatetext.configuration.gcloud_syncer import GCloudSync 
from Hatetext.components.data_ingestion import DataIngestion
from Hatetext.components.data_transformation import DataTransformation 
from Hatetext.entity.config_entity import DataTransformationConfig
from Hatetext.entity.artifact_entity import DataIngestionArtifacts


class PredictionPipeline:
    def __init__(self):
        self.bucket_name=BUCKET_NAME
        self.model_name=MODEL_NAME
        self.model_path=os.path.join("artifacts","PredictModel")
        self.gcloud=GCloudSync()
        self.data_tranformation=DataTransformation(data_transformation_config=DataTransformationConfig, data_ingestion_artifacts=DataIngestionArtifacts)


    def get_model_from_gcloud(self) -> str:

        logging.info("Entered the get_model_from_gcloud method to fetch the model from gcloud")
        try:
            # Model file exists, load the model
            model_path = '/Users/ravina/Desktop/EndtoEndTextclassification/artifacts/PredictModel/model.h5'
            if os.path.exists(model_path):
                best_model_path = keras.models.load_model(model_path) 
            
            #loading the best model from S3 bucket
            else:  
                os.makedirs(self.model_path,exist_ok=True)
                self.gcloud.sync_folder_from_gcloud(self.bucket_name,self.model_name,self.model_path)
                best_model_path=os.path.join(self.model_path,self.model_name)
            
            logging.info("Exited the get_model_from_gcloud method of prediction pipeline")
            return best_model_path
        except Exception as e:
            raise CustomException(e,sys) from e

    def predict(self,best_model_path,text):
        logging.info("Started running the predict function")
        try:
            model_path = '/Users/ravina/Desktop/EndtoEndTextclassification/artifacts/PredictModel/model.h5'
            if os.path.exists(model_path):
                # Model file exists, load the model
                load_model = keras.models.load_model(model_path) 
            else:
                best_model_path:str=self.get_model_from_gcloud()
                load_model=keras.models.load_model(best_model_path)
            
            with open('tokenizer.pickle','rb') as handle:
                load_tokenizer=pickle.load(handle)
            
            text=self.data_tranformation.data_cleaning(text)
            text=[text]
            print(text)
            seq=load_tokenizer.texts_to_sequences(text)
            padded=pad_sequences(seq,maxlen=300)
            print(seq)
            pred=load_model.predict(padded)
            pred
            print("pred",pred)
            if pred>0.5:
                print("Hate and abusive")
                return "Hate and abusive"
            
            else:
                print("not hateful")
                return "not hateful"
        except Exception as e:
            raise CustomException (e,sys) from e


    def run_pipeline(self,text):
        logging.info("Entered the run_pipeline method of PredictionPipeline Class")
        try:
            best_model_path: str= self.get_model_from_gcloud()
            predicted_text=self.predict(best_model_path,text)

            logging.info("Exited the run_pipeline method of PredictionPipeline Class")
            return predicted_text
        
        except Exception as e:
            raise CustomException(e,sys) from e

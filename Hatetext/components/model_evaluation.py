import os 
import sys
import pickle
import keras
import numpy as np
import pandas as pd
from Hatetext.logger import logging
from Hatetext.exception import CustomException
from Hatetext.constant import *
from Hatetext.configuration.gcloud_syncer import GCloudSync
from sklearn.metrics import confusion_matrix
from Hatetext.entity.config_entity import ModelEvaluationConfig
from Hatetext.entity.artifact_entity import ModelEvaluationArtifacts,ModelTrainerArtifacts,DataTransformationArtifacts
from keras.utils import pad_sequences


class ModelEvaluation:

    def __init__(self,model_evaluation_config: ModelEvaluationConfig,
                 model_trainer_artifacts: ModelTrainerArtifacts,
                 data_transformation_artifacts:DataTransformationArtifacts):
        
        """
        model evaluation part
        """

        self.model_evaluation_config=model_evaluation_config
        self.model_trainer_artifacts=model_trainer_artifacts
        self.data_transformation_artifacts=data_transformation_artifacts
        self.gcloud=GCloudSync()


    def get_the_best_model_from_gcloud(self) ->str:
        """
        this will fetch the best model from gcloud storage and store inside best model diretory
       
        """
        try:
            logging.info("entered into get_the_best_model method of ModelEvaluation class")

            os.makedirs(self.model_evaluation_config.BEST_MODEL_DIR_PATH,exist_ok=True)

            self.gcloud.sync_folder_from_gcloud(self.model_evaluation_config.BUCKET_NAME,
                                                self.model_evaluation_config.MODEL_NAME,
                                                self.model_evaluation_config.BEST_MODEL_DIR_PATH)
            best_model_path=os.path.join(self.model_evaluation_config.BEST_MODEL_DIR_PATH,self.model_evaluation_config.MODEL_NAME)
            
            logging.info("exited from the get_the_best_model method")

            return best_model_path
        except Exception as e:
            raise CustomException(e,sys) from e
        
    
    def evaluate(self):
        """
        parameters: currently trained model and model from gcloud
        param data loader: Data loader for validation dataset
        return: loss incurred
        """

        try:
            logging.info("enter inside evaluate method of ModelEvaluation class")
            print(self.model_trainer_artifacts.x_test_path)
            X_test=pd.read_csv(self.model_trainer_artifacts.x_test_path,index_col=0)
            print(X_test)
            y_test=pd.read_csv(self.model_trainer_artifacts.y_test_path,index_col=0)

            with open('tokenizer.pickle','rb') as handle:
                tokenizer=pickle.load(handle)
            
            load_model=keras.models.load_model(self.model_trainer_artifacts.trained_model_path)

            X_test=X_test['tweet'].astype(str)

            X_test=X_test.squeeze()
            y_test=y_test.squeeze()

            test_sequences=tokenizer.texts_to_sequences(X_test)
            test_sequences_matrix=pad_sequences(test_sequences,maxlen=MAX_LEN)

            print(f"------{test_sequences_matrix}--------")
            print(f"-------{X_test.shape}----------------")
            print(f"-------{y_test.shape}----------------")

            accuracy=load_model.predict(test_sequences_matrix,y_test)

            logging.info(f"test accuracy is: ---{accuracy}")
            model_prediction=load_model.predict(test_sequences_matrix)

            res=[]
            for prediction in model_prediction:
                if prediction[0]<0.5:
                    res.append(0)
                else:
                    res.append(1)
            
            #print(confusion_matrix(res,y_test))

            logging.info(f"Confusion matrix is {confusion_matrix(res,y_test)}")
            return accuracy
        except Exception as e:
            raise CustomException(e,sys) from e



    def initiate_model_evaluation(self) -> ModelEvaluationArtifacts:
        """
        This method is used to initiate all tghe steps of model_evaluation function
        Output: Returns model evalution artifacts
        on Failure: Write an exception log to capture any exceptions arised
        """
        logging.info("initate the model_evaluation method")

        try:
            trained_model=keras.models.load_model(self.model_trainer_artifacts.trained_model_path)
            with open('tokenizer.pickle','rb') as handle:
                load_tokenizer=pickle.load(handle)
            
            trained_model_accuracy=self.evaluate()

            logging.info("Fetch best model from gcloud storage")
            best_model_path=self.get_the_best_model_from_gcloud()

            logging.info("verify if best model present in gcloud or not")
            if os.path.isfile(best_model_path) is False:
                is_model_accepted=True
            
                logging.info("gcloud model is not best and curently trained model is accepted")

            else:
                logging.info("best model fetched from gcloud")
                best_model=keras.models.load_model(best_model_path)
                best_model_accuracy=self.evaluate()

                logging.info("comparing the loss betwee best_model_loss and trained_model_loss")
                if best_model_accuracy> trained_model_accuracy:
                    is_model_accepted=True
                    logging.info("gcloud model is accepted")
                else:
                    is_model_accepted=False
                    logging.info("trained local model is accepted")
                
            
            model_evaluation_artifacts=ModelEvaluationArtifacts(is_model_accepted=is_model_accepted)
            logging.info("returning ModelEvaluationArtifacts")

            return model_evaluation_artifacts



        except Exception as e:
            raise CustomException(e,sys) from e




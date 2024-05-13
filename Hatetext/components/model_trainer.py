import os
import sys
import pickle 
import pandas as pd 
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from Hatetext.logger import logging
from Hatetext.constant import *
from Hatetext.exception import CustomException
from Hatetext.entity.config_entity import ModelTrainerConfig
from Hatetext.entity.artifact_entity import ModelTrainerArtifacts,DataTransformationArtifacts
from Hatetext.ml.model import ModelArchitechure
import tensorflow.keras.losses as losses
loss_function = losses.BinaryCrossentropy()




class ModelTrainer:
    def __init__(self,data_transformation_artifacts: DataTransformationArtifacts,
                 model_trainer_config: ModelTrainerConfig):
        self.data_transformation_artifacts=data_transformation_artifacts
        self.model_trainer_config=model_trainer_config

    def split_data(self,csv_path):
        try:
            logging.info("start splitting the data into the split_data function")
            df=pd.read_csv(csv_path,index_col=False)
            logging.info("splitting the data into X and Y")
            X=df[TWEET]
            y=df[LABEL]

            logging.info("applying train test split on the data X and y")
            X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=RANDOM_STATE)
            print(len(X_train),len(y_train))
            print(len(X_test),len(y_test))
            print(type(X_train),type(y_train))

            logging.info("data splitting done")
            return X_train,X_test,y_train,y_test
        
        except Exception as e:
            raise CustomException(e,sys) from e
        
    
    def tokenize_data(self,X_train):
        try:
            logging.info("Apply tokenization to create integer encodings")
            tokenizer=Tokenizer(num_words=self.model_trainer_config.MAX_WORDS)
            tokenizer.fit_on_texts(X_train)
            sequences=tokenizer.texts_to_sequences(X_train)
            logging.info("Converting text to sequences: {sequences}")
            sequences_matrix=pad_sequences(sequences,maxlen=self.model_trainer_config.MAX_LEN)
            logging.info("the sequences matrix is :{sequences_matrix}")
            return sequences_matrix,tokenizer
        except Exception as e:
            raise CustomException(e, sys) from e
        

    
    def initiate_model_trainer(self,) -> ModelTrainerArtifacts:
        logging.info("Entered into the inititate_model_trainer method in the ModelTrainerClass")

        """
        method name: initiate_model_trainer
        Description: this method will intiate the model trainer steps
        output: Returns ModelTrainerArtifacts
        On failure: write the code inside try except blog and write the exception log
        """
        
        try:
            logging.info("model trainer started")

            X_train,X_test,y_train,y_test=self.split_data(csv_path=self.data_transformation_artifacts.transformed_data_path)
            model_architechure=ModelArchitechure()
            model=model_architechure.get_model()

            logging.info(f"X_train size is : {X_train.shape}, and X_test size is :{X_test.shape}")

            sequences_matrix,tokenizer=self.tokenize_data(X_train)

            logging.info("Model training started")
            model.fit(sequences_matrix, y_train,
                      batch_size=self.model_trainer_config.BATCH_SIZE,
                      epochs=self.model_trainer_config.EPOCH,
                      validation_split=self.model_trainer_config.VALIDATION_SPLIT)
            logging.info("Model training finished")

            with open("tokenizer.pickle","wb") as handle:
                pickle.dump(tokenizer,handle, protocol=pickle.HIGHEST_PROTOCOL)
            os.makedirs(self.model_trainer_config.TRAINED_MODEL_DIR,exist_ok=True)


            logging.info("saving the trained model")
            model.save(self.model_trainer_config.TRAINED_MODEL_PATH)
            X_train.to_csv(self.model_trainer_config.X_TRAIN_DATA_PATH)

            X_test.to_csv(self.model_trainer_config.X_TEST_DATA_PATH)
            y_test.to_csv(self.model_trainer_config.Y_TEST_DATA_PATH)

            model_trainer_artifacts=ModelTrainerArtifacts(
                trained_model_path=self.model_trainer_config.TRAINED_MODEL_PATH,
                x_test_path=self.model_trainer_config.X_TEST_DATA_PATH,
                y_test_path=self.model_trainer_config.Y_TEST_DATA_PATH
            )

            logging.info("Retirning the ModelTrainerArtifacts")

            return model_trainer_artifacts
        
        except Exception as e:
            raise CustomException(e, sys) from e

            
import os 
from datetime import datetime
import tensorflow.keras.losses as losses
loss_function = losses.BinaryCrossentropy()


TIMESTAMP=datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
ARTIFACTS_DIR=os.path.join("artifacts",TIMESTAMP)


#common constant variables for project 
BUCKET_NAME="hatespeech-project"
ZIP_FILE_NAME="dataset.zip"
LABEL='label'
TWEET="tweet"

# Data ingestion related constants

DATA_INGESTION_ARTIFACTS_DIR="DataIngestionArtifacts"
DATA_INGESTION_IMBALANCE_DATA_DIR="Imbalanced_data.csv"
DATA_INGESTION_RAW_DATA_DIR="raw_data.csv"


# Data transformation related constants
DATA_TRANSFORMATION_ARTIFACTS_DIR='DatatransformationArtifacts'
TRANSFORMED_FILE_NAME='final.csv'
DATA_DIR='data'
ID='id'
AXIS=1
INPLACE=True
DROP_COLUMNS=["Unnamed: 0","count","hate_speech","offensive_language","neither"]
CLASS='class'

#Model trainer constants
MODEL_TRAINER_ARTIFACTS_DIR="ModelTrainerArtifacts"
TRAINED_MODEL_DIR="trained_model"
TRAINED_MODEL_NAME="model.h5"
X_TEST_FILE_NAME="x_test.csv"
Y_TEST_FILE_NAME="y_test.csv"
X_TRAIN_FILE_NAME="X_train.csv"
RANDOM_STATE=42
EPOCH=1
BATCH_SIZE=128
VALIDATION_SPLIT=0.20

#MODEL ARCHITECHURE CONSTANTS
MAX_WORDS=500000
MAX_LEN=300
LOSS=loss_function
METRICS=['accuracy']
ACTIVATION="sigmoid"

#Model evaluation constants
MODEL_EVALUATION_ARTIFACTS_DIR='ModelEvaluationArtifacts'
BEST_MODEL_DIR='best_model'
MODEL_EVALUATION_FILE_NAME='loss.csv'

MODEL_NAME='model.h5'
APP_HOST='0.0.0.0'
APP_PORT=8000

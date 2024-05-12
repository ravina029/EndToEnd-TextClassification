import sys
from Hatetext.logger import logging
from Hatetext.exception import CustomException
from Hatetext.components.data_ingestion import DataIngestion 
from Hatetext.entity.config_entity import DataIngestionConfig
from Hatetext.entity.artifact_entity import DataIngestionArtifacts


class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()

    
    def start_data_ingestion(self)-> DataIngestionArtifacts:
        logging.info("Entered into start_data_ingestion method of TrainPipeline class")
        data_inestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)

        data_inestion_artifacts=data_inestion.initiate_data_ingestion()
        logging.info("got train and validation datasets from gcloud storage")
        logging.info("exited from start_data_ingestion method of Training pipeline")

        return data_inestion_artifacts
    

    def run_puipeline(self):
        logging.info("Entered into run_pipeline method of the Training pipeline")
        try: 
            data_inestion_artifacts=self.start_data_ingestion()
        
            logging.info("Exited from run_pipeline method of the Training pipeline")

        except Exception as e:
            raise CustomException(e,sys) from e 


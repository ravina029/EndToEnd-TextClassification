import os 
import sys 
from zipfile import ZipFile
from Hatetext.logger import logging
from Hatetext.exception import CustomException
from Hatetext.configuration.gcloud_syncer import GCloudSync
from Hatetext.entity.config_entity import DataIngestionConfig
from Hatetext.entity.artifact_entity import DataIngestionArtifacts



class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config=data_ingestion_config
        self.gcloud=GCloudSync()


    def get_data_from_gcloud(self) -> None:
        try:
            logging.info("Entered into get_data_from_gcloud class method")
            os.makedirs(self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR,exist_ok=True)

            self.gcloud.sync_folder_from_gcloud(self.data_ingestion_config.BUCKET_NAME,
                                                self.data_ingestion_config.ZIP_FILE_NAME,
                                                self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR,
                                                )
            
            logging.info("Exited from get_data_from_gcloud class")

        except Exception as e:
            raise CustomException(e,sys) from e
        
    def unzip_and_clean(self):
        logging.info("Entered into unzip_and_clean class method")
        try: 
            with ZipFile(self.data_ingestion_config.ZIP_FILE_PATH,"r") as zip_ref:
                zip_ref.extractall(self.data_ingestion_config.ZIP_FILE_DIR)
            
            logging.info("Exiting from unzip_and_clean class method")

            return self.data_ingestion_config.DATA_ARTIFACTS_DIR,self.data_ingestion_config.NEW_DATA_ARTIFACTS_DIR

        except Exception as e:
            raise CustomException(e,sys) from e
        
    
    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        try:
            self.get_data_from_gcloud()
            logging.info("fetched the data from g_cloud")
            imbalanced_data_file_path,raw_data_file_path=self.unzip_and_clean()
            logging.info("Unzip file and split onto train and val data")

            data_ingestion_artifacts=DataIngestionArtifacts(
                imbalanced_data_file_path=imbalanced_data_file_path,
                raw_data_file_path=raw_data_file_path
            )

            logging.info("exited from initiate_data_ingestion method of DataIngestion Class")
            logging.info(f"Data ingestion Artifact:{data_ingestion_artifacts}")

            return data_ingestion_artifacts


        except Exception as e:
            raise CustomException(e,sys) from e


        

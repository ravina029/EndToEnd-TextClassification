import sys 
import os 
from Hatetext.logger import logging
from Hatetext.exception import CustomException
from Hatetext.configuration.gcloud_syncer import GCloudSync
from Hatetext.entity.config_entity import ModelPusherConfig
from Hatetext.entity.artifact_entity import ModelPusherArtifacts


class ModelPusher:
    def __init__(self,model_pusher_config: ModelPusherConfig):
        """
        model pusher config: Configuration for the model pusher
        """
        self.model_pusher_config=model_pusher_config
        self.gcloud=GCloudSync()


    def initiate_model_pusher(self) ->ModelPusherArtifacts:
        """
        About: this method will inittiate model pusher.
        Output: Model pusher artifact
        """
        try:
            self.gcloud.sync_folder_to_gcloud(self.model_pusher_config.BUCKET_NAME,
                                              self.model_pusher_config.TRAINED_MODEL_PATH,
                                              self.model_pusher_config.MODEL_NAME)
            
            logging.info("Uploaded the best model to the gcloud storage")

            #saving model pusher

            model_pusher_artifact=ModelPusherArtifacts(
                bucket_name=self.model_pusher_config.BUCKET_NAME
            )
            logging.info("exit the initiate_model_pusher method")

            return model_pusher_artifact
        
        except Exception as e:
            raise CustomException(e,sys) from e
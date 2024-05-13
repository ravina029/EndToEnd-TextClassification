import sys
import os 
from Hatetext.logger import logging
from Hatetext.exception import CustomException
from Hatetext.components.data_ingestion import DataIngestion
from Hatetext.components.data_transformation import DataTransformation 
from Hatetext.entity.config_entity import DataIngestionConfig,DataTransformationConfig,ModelTrainerConfig,ModelEvaluationConfig,ModelPusherConfig
from Hatetext.entity.artifact_entity import DataIngestionArtifacts,DataTransformationArtifacts,ModelTrainerArtifacts,ModelEvaluationArtifacts,ModelPusherArtifacts
from Hatetext.components.model_trainer import ModelTrainer
from Hatetext.components.model_evaluation import ModelEvaluation
from Hatetext.components.model_pusher import ModelPusher


class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()
        self.data_transformation_config=DataTransformationConfig()
        self.model_trainer_config=ModelTrainerConfig()
        self.model_evaluation_config=ModelEvaluationConfig()
        self.model_pusher_config=ModelPusherConfig()

    
    def start_data_ingestion(self)-> DataIngestionArtifacts:
        logging.info("Entered into start_data_ingestion method of TrainPipeline class")
        data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)

        data_ingestion_artifacts=data_ingestion.initiate_data_ingestion()
        logging.info("got train and validation datasets from gcloud storage")
        logging.info("exited from start_data_ingestion method of Training pipeline")

        return data_ingestion_artifacts
    

    def start_data_transformation(self,data_ingestion_artifacts=DataIngestionArtifacts) ->DataTransformationArtifacts:
        logging.info("Initializing the data transfornmation methods in the training pipeline")
        try:
            data_transformation=DataTransformation(data_ingestion_artifacts=data_ingestion_artifacts,data_transformation_config=self.data_transformation_config)


            data_transformation_artifacts=data_transformation.initiate_data_transformation()
            logging.info('exited the start_data_transformation method of training pipeline')

            return data_transformation_artifacts
        except Exception as e:
            raise CustomException(e,sys) from e
    

    def start_model_trainer(self,data_transformation_artifacts: DataTransformationArtifacts) ->ModelTrainerArtifacts:
        logging.info("Entered the model_trainer method of training pipeline")

        try: 
            model_trainer=ModelTrainer(data_transformation_artifacts=data_transformation_artifacts,
                                       model_trainer_config=self.model_trainer_config)
            
            model_trainer_artifacts=model_trainer.initiate_model_trainer()
            logging.info("exited the strst_model_trainer method in training pipeline class")
            return model_trainer_artifacts
            
        except Exception as e:
            raise CustomException(e,sys) from e
            
    def start_model_evalution(self,model_trainer_artifacts: ModelTrainerArtifacts,data_transformation_artifacts: DataTransformationArtifacts):
        logging.info("Entered inside start_model_evalution method of trainig pipeline class")
        try:
            model_evaluation=ModelEvaluation(data_transformation_artifacts=data_transformation_artifacts,
                                             model_evaluation_config=self.model_evaluation_config,
                                             model_trainer_artifacts=model_trainer_artifacts)
            
            model_evaluation_artifacts=model_evaluation.initiate_model_evaluation()
            logging.info("exited the start_model_evalution method of trainig pipeline class")
            return model_evaluation_artifacts

        except Exception as e:
            raise CustomException(e,sys) from e


    def  start_model_pusher(self,) -> ModelPusherArtifacts:
        logging.info("Entered inside start_model_pusher method of Training pipline ")
        try:
            model_pusher=ModelPusher(model_pusher_config=self.model_evaluation_config,)

            model_pusher_artifact=model_pusher.initiate_model_pusher()
            logging.info("initiated the model pusher and exited the start_model_pusher methos of training pipeline")
            return model_pusher_artifact
        
        except Exception as e:
            raise CustomException(e,sys) from e




    def run_pipeline(self):
        logging.info("Entered into run_pipeline method of the Training pipeline")
        try: 
            data_ingestion_artifacts=self.start_data_ingestion()
            data_transformation_artifacts=self.start_data_transformation(data_ingestion_artifacts=data_ingestion_artifacts)
            model_trainer_artifacts=self.start_model_trainer(data_transformation_artifacts=data_transformation_artifacts)
            model_evaluation_artifacts=self.start_model_evalution(model_trainer_artifacts,data_transformation_artifacts=data_transformation_artifacts)


            if not model_evaluation_artifacts.is_model_accepted:
                raise Exception("trained model is not better than best gcloud model")
            model_pusher_artifacts=self.start_model_pusher()


            logging.info("Exited from run_pipeline method of the Training pipeline")

        except Exception as e:
            raise CustomException(e,sys) from e 



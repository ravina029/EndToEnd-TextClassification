import pandas as pd 
import nltk
import string
import os
import sys 
import re
from nltk.corpus import stopwords
nltk.download('stopwords')
from sklearn.model_selection import train_test_split

from Hatetext.logger import logging
from Hatetext.exception import CustomException
from Hatetext.entity.config_entity import DataTransformationConfig
from Hatetext.entity.artifact_entity import DataIngestionArtifacts,DataTransformationArtifacts


class DataTransformation:
    def __init__(self,data_transformation_config: DataTransformationConfig, data_ingestion_artifacts:DataIngestionArtifacts):
        self.data_transformation_config=data_transformation_config
        self.data_ingestion_arifacts=data_ingestion_artifacts

    def imbalanced_data_cleaning(self):
        try:
            logging.info("Strated cleaning the imbalanced data")
            imbalanced_data=pd.read_csv(self.data_ingestion_arifacts.imbalanced_data_file_path)
            imbalanced_data.drop(self.data_transformation_config.ID,axis=self.data_transformation_config.AXIS,inplace=self.data_transformation_config.INPLACE)
            logging.info(f'dropped the unneccessary column ID and return imbalanced data {imbalanced_data}')

            return imbalanced_data
        except Exception as e:
            raise CustomException(e,sys) from e
        
    def raw_data_cleaning(self):
        try:
            logging.info("Strated cleaning the raw data")
            raw_data=pd.read_csv(self.data_ingestion_arifacts.raw_data_file_path)
            raw_data.drop(self.data_transformation_config.DROP_COLUMNS,axis=self.data_transformation_config.AXIS,inplace=self.data_transformation_config.INPLACE)
            raw_data[raw_data[self.data_transformation_config.CLASS]==0][self.data_transformation_config.CLASS]==1 #copy class 1 into 0
            raw_data[self.data_transformation_config.CLASS].replace({0:1},inplace=True) #replace 0 with 1
            raw_data[self.data_transformation_config.CLASS].replace({2:0},inplace=True) #replace 2 with 0
            raw_data.rename(columns={self.data_transformation_config.CLASS:self.data_transformation_config.LABEL},inplace=True)
            
            logging.info(f'tranformed raw data is {raw_data}')

            return raw_data
        except Exception as e:
            raise CustomException(e,sys) from e
        
    
    def concat_dataframe(self):
       try:
           logging.info("entered into concatenation method of the datatrnasformation class")
           df_list=[self.raw_data_cleaning(),self.imbalanced_data_cleaning()]
           df=pd.concat(df_list)
           print(df.head())
           print(df.shape)
           logging.info(f"done with concatinating the dataframe  and returned final dataframe {df}")
           return df 
       
       except Exception as e:
           raise CustomException(e,sys) from e
       
    def data_cleaning(self,text):
        try:
            logging.info("Started text cleaning or text preprocessing")
            #apply stemming and stopword on the data df
            stemmer=nltk.SnowballStemmer('english')
            stopword=set(stopwords.words('english')) #we will remove these stopwords from our data

            text=str(text).strip()
            text=str(text).lower()
            text=re.sub('\[.*?\]','',text)
            text=re.sub("https?://\S+|www\.\S+","",text)
            text=re.sub("<.*?>+","",text)
            text=re.sub("[%s]" %re.escape(string.punctuation),"",text)
            text=re.sub("\n",'',text)
            text=re.sub("\w*\d\w*","",text)
            text=[word for word in text.split(' ') if text not in stopword]
            text="  ".join(text)
            text=[stemmer.stem(text) for word in text.split(' ')]
            text="  ".join(text)

            return text
        except Exception as e:
            raise CustomException(e,sys) from e
        

    def initiate_data_transformation(self) ->DataIngestionArtifacts:
        try:
            logging.info("Initializing the data transfornmation methods")
            self.imbalanced_data_cleaning()
            self.raw_data_cleaning()
            df=self.concat_dataframe()
            df[self.data_transformation_config.TWEET]=df[self.data_transformation_config.TWEET].apply(self.data_cleaning)

            os.makedirs(self.data_transformation_config.DATA_TRANSFORMATION_ARTIFACTS_DIR,exist_ok=True)
            df.to_csv(self.data_transformation_config.TRANSFORMED_FILE_PATH,index=False,header=True)

            data_transformation_artifact=DataTransformationArtifacts(transformed_data_path=self.data_transformation_config.TRANSFORMED_FILE_PATH)
            logging.info('returned the DataTransformationArtifacts')

            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys) from e
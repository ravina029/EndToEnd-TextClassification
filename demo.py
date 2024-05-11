from Hatetext.logger import logging
from Hatetext.exception import CustomException
import sys
from Hatetext.configuration.gcloud_syncer import GCloudSync 

obj=GCloudSync()
obj.sync_folder_from_gcloud("hatespeech-project","dataset.zip",'downloaded/dataset.zip')
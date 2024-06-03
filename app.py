from Hatetext.pipeline.train_pipeline import TrainPipeline

from fastapi import FastAPI
import uvicorn
import sys
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.responses import Response
from Hatetext.pipeline.prediction_pipeline import PredictionPipeline
from Hatetext.exception import CustomException
from Hatetext.constant import *


text:str = "Welcome to your first programme of fastapi"
app = FastAPI()

@app.get("/", tags=['authentication'])
async def index():
    return RedirectResponse(url='/docs')

@app.get("/train")
async def training():
    try:
        train_pipeline=TrainPipeline()
        train_pipeline.run_pipeline()

        return Response("Training sucessfull.")
    except Exception as e:
        return Response(f"Error Occured: {e}")
    
@app.get("/predict")
async def predict_route(text):
    try:
        obj = PredictionPipeline()
        text = obj.run_pipeline(text)
        return text

    except Exception as e:
        raise CustomException (e,sys) from e
    

if __name__=="__main__":
    uvicorn.run(app,host=APP_HOST,port=APP_PORT)
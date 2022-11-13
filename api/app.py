import uvicorn
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import Body, FastAPI
from fastapi import FastAPI, HTTPException
import json
import pickle
from fastapi.encoders import jsonable_encoder
from joblib import dump, load
#from fastapi.encoders import jsonable_encoder
#from fastapi.responses import JSONResponse

description = """
GetAround Pricing API
"""

tags_metadata = [

    {
        "name": "Preview",
        "description": "Endpoints that quickly explore dataset"
    },

    {
        "name": "Prediction",
        "description": "Rental Pricing prediction based on my model"
    }
]

app = FastAPI(
    title="🚗 GetAround API",
    description=description,
    version="0.1",
    contact={
        "name": "GetAround API by Frederic PRIGENT",
        "url": "https://github.com/dafrd",
    },
    openapi_tags=tags_metadata
)

class PredictionFeatures(BaseModel):
    model_key: object
    mileage: Union[int, float]
    engine_power: Union[int, float]
    fuel:object
    paint_color:object
    car_type:object
    private_parking_available:bool  
    has_gps:bool  
    has_air_conditioning:bool  
    automatic_car:bool  
    has_getaround_connect: bool  
    has_speed_regulator:bool  
    winter_tires:bool  

@app.get("/preview", tags=["Preview"])
async def sample(rows: int=10):
    """
    Get a sample of your whole dataset. 
    You can specify how many rows you want by specifying a value for `rows`, default is `10`
    """
    df = pd.read_csv("get_around_pricing_project.csv",index_col=0)
    sample = df.sample(rows)
    return sample.to_json(orient='records')

@app.post("/predict", tags=["Prediction"])
async def predict(predictionFeatures:PredictionFeatures):
#async def predict(predictionFeatures:PredictionFeatures=Body(embed=True)):    
    """
    Rental price prediction based on car characteristics
    """
    #json_compatible_item_data = jsonable_encoder(predictionFeatures)
    df = pd.DataFrame(dict(predictionFeatures), index=[0])
    #model = pickle.load(open('getaround_model.pkl','rb'))

    #features = predictionFeatures.dict()
    # model_key = features['model_key']
    # mileage = features['mileage']
    # engine_power = features['engine_power']
    # fuel = features['fuel']
    # paint_color = features['paint_color']
    # car_type = features['car_type']
    # private_parking_available = features['private_parking_available']
    # has_gps = features['has_gps']
    # has_air_conditioning = features['has_air_conditioning']
    # automatic_car = features['automatic_car']
    # has_getaround_connect = features['has_getaround_connect']
    # has_speed_regulator = features['has_speed_regulator']
    # winter_tires = features['winter_tires']

    with open('getaround_model.pkl', 'rb') as f:
          getaround_model = pickle.load(f)

    prediction = getaround_model.predict(df)
    response = {"Rental car pricing based on the car info":prediction.tolist()[0]}

    #df = pd.DataFrame(dict(predictionFeatures), index=[0])

    # loaded_model = load('getaround_model.joblib')
    #prediction = loaded_model.predict(df)
    # response = {"Rental car pricing based on the car info":prediction.tolist()[0]}
    return response

# @app.exception_handler(500)
# async def internal_exception_handler(request: Request, exc: Exception):
#   return JSONResponse(status_code=500, content=jsonable_encoder({"code": 500, "msg": "Internal Server Error"}))

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000, debug=True, reload=True)
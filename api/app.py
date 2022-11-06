import uvicorn
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List
from fastapi import Body, FastAPI
import json
import pickle

description = """
GetAround Pricing API
"""

tags_metadata = [

    {
        "name": "Preview",
        "description": "Endpoints that quickly explore dataset",
    },

    {
        "name": "Prediction",
        "description": "Rental Pricing prediction based on our model"
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
    model_key:str
    mileage:int
    engine_power:int
    fuel:str
    paint_color:str
    car_type:str
    private_parking_available:bool
    has_gps:bool
    has_air_conditioning:bool
    automatic_car:bool
    has_getaround_connect:bool
    has_speed_regulator:bool
    winter_tires:bool

@app.get("/preview", tags=["Preview"])
async def sample(rows: int=10):
    """
    Get a sample of your whole dataset. 
    You can specify how many rows you want by specifying a value for `rows`, default is `10`
    """
    df = pd.read_csv("get_around_pricing_project.csv")
    sample = df.sample(rows)
    return sample.to_json()

@app.post("/predict", tags=["Prediction"])
async def predict(predictionFeatures:PredictionFeatures,item: PredictionFeatures = Body(embed=True)):
    """
    Rental price prediction based on car characteristics
    """
    df = pd.DataFrame(dict(predictionFeatures), index=[0])
    #model = pickle.load(open('getaround_model.pkl','rb'))
    getaround_model = pickle.load(open('getaround_model.pkl','rb'))
    prediction = getaround_model.predict(df)
    response = {"Rental car pricing based on the car info":prediction.tolist()[0]}
    return response

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000, debug=True, reload=True)
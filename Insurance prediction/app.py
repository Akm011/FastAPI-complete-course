from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pickle
import pandas as pd

# import the ml model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

#MLFlow model version
MODEL_VERSION = "1.0.0"

app = FastAPI()

#human readable routes
@app.get('/')
def home():
    return JSONResponse(status_code=200, content={'message': 'Welcome to the Insurance Premium Prediction API!'})

#machine readable health check route
@app.get('/health')
def health_check():
    return JSONResponse(status_code=200, content={'status': 'API is healthy and running!', 'model_version': MODEL_VERSION, 'model_loaded': model is not None})

@app.post('/predict')
def predict_premium(data: UserInput):

    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])

    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={'predicted_category': prediction})

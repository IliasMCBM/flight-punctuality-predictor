from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

# Load the model from joblib
loaded_pipeline = joblib.load('xgboost_model.joblib')
df = pd.read_csv('combined_2023.csv')
distances_dict = df.groupby(['ORIGIN', 'DEST'])['DISTANCE'].mean().to_dict()

# Define the expected data structure
class InputData(BaseModel):
    origin: str
    destination: str
    month: int
    day: int
    departure_time: int
    arrival_time: int

# Initialize the FastAPI app
app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:5003",  # Add your frontend URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Route to receive form data and make predictions
@app.post('/prediction')
async def get_prediction(data: InputData):
    try:
        # Get the distance from the dictionary
        distance = distances_dict.get((data.origin, data.destination), None)

        if distance is None:
            return {"error": "No distance found for the provided origin and destination"}

        # Prepare the data for prediction
        inputs = [
            [2024, data.month, data.day, data.origin, data.destination, data.departure_time, data.arrival_time, distance]
        ]

        # Convert inputs into a DataFrame for the model
        input_df = pd.DataFrame(inputs, columns=['YEAR', 'MONTH', 'DAY_OF_WEEK', 'ORIGIN', 'DEST', 'CRS_DEP_TIME',
                                                 'CRS_ARR_TIME', 'DISTANCE'])

        # Make predictions with the loaded model
        predictions = loaded_pipeline.predict(input_df)
        probabilities = loaded_pipeline.predict_proba(input_df)[:, 1]  # Probability of the positive class

        # Convert predictions and probabilities to types that FastAPI can handle
        predictions = predictions.tolist()  # Convert numpy array to Python list
        probabilities = probabilities.tolist()  # Convert numpy array to Python list

        # Format the response
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            results.append({
                "Input": i + 1,
                "Prediction": int(pred),
                "Probability of being 1": round(prob, 4),
                "Distance": distance
            })

        return results

    except Exception as e:
        return {"error": str(e)}

# To start the server, use the command: uvicorn app:app --reload --port 8001
#python -m http.server 5001


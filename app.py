from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

# Cargar el modelo desde joblib
loaded_pipeline = joblib.load('xgboost_model.joblib')
df = pd.read_csv('combined_2023.csv')
distances_dict = df.groupby(['ORIGIN', 'DEST'])['DISTANCE'].mean().to_dict()

# Definir la estructura de datos esperada
class DatosEntrada(BaseModel):
    origen: str
    destino: str
    mes: int
    dia: int
    hora_salida: int
    hora_llegada: int

# Inicializar la aplicación FastAPI
app = FastAPI()

# Configurar CORS
origins = [
    "http://localhost",
    "http://localhost:5002",  # Agrega aquí la URL de tu frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Ruta para recibir los datos del formulario y hacer la predicción
@app.post('/prediccion')
async def obtener_prediccion(datos: DatosEntrada):
    try:
        # Obtener la distancia desde el diccionario
        distance = distances_dict.get((datos.origen, datos.destino), None)

        if distance is None:
            return {"error": "No se encontró la distancia para el origen y destino proporcionados"}

        # Preparar los datos para hacer la predicción
        inputs = [
            [2024, datos.mes, datos.dia, datos.origen, datos.destino, datos.hora_salida, datos.hora_llegada, distance]
        ]

        # Convertir inputs en un DataFrame para usarlo con el modelo
        input_df = pd.DataFrame(inputs, columns=['YEAR', 'MONTH', 'DAY_OF_WEEK', 'ORIGIN', 'DEST', 'CRS_DEP_TIME',
                                                 'CRS_ARR_TIME', 'DISTANCE'])

        # Realizar predicciones con el modelo cargado
        predictions = loaded_pipeline.predict(input_df)
        probabilities = loaded_pipeline.predict_proba(input_df)[:, 1]  # Probabilidad de la clase positiva

        # Convertir predicciones y probabilidades a tipos de datos que fastapi pueda manejar
        predictions = predictions.tolist()  # Convertir numpy array a lista de Python
        probabilities = probabilities.tolist()  # Convertir numpy array a lista de Python

        # Formatear la respuesta
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            results.append({
                "Input": i + 1,
                "Predicción": int(pred),
                "Probabilidad de ser 1": round(prob, 4),
                "Distancia": distance
            })

        return results

    except Exception as e:
        return {"error": str(e)}

# Para iniciar el servidor, usa el comando: uvicorn app:app --reload --port 8001
    #python -m http.server 5001

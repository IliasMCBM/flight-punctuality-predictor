from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Cargar el modelo desde joblib
loaded_pipeline = joblib.load('xgboost_model.joblib')


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


# Ruta para recibir los datos del formulario y hacer la predicción
@app.post('/prediccion')
async def obtener_prediccion(datos: DatosEntrada):
    try:
        # Preparar los datos para hacer la predicción
        inputs = [
            [2024, datos.mes, datos.dia, datos.origen, datos.destino, datos.hora_salida, datos.hora_llegada, 100000]
        ]

        # Convertir inputs en un DataFrame para usarlo con el modelo
        input_df = pd.DataFrame(inputs, columns=['YEAR', 'MONTH', 'DAY_OF_WEEK', 'ORIGIN', 'DEST', 'CRS_DEP_TIME',
                                                 'CRS_ARR_TIME', 'DISTANCE'])

        # Realizar predicciones con el modelo cargado
        predictions = loaded_pipeline.predict(input_df)
        probabilities = loaded_pipeline.predict_proba(input_df)[:, 1]  # Probabilidad de la clase positiva

        # Formatear la respuesta
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            results.append({
                "Input": i + 1,
                "Predicción": int(pred),
                "Probabilidad de ser 1": round(prob, 4)
            })

        return results

    except Exception as e:
        return {"error": str(e)}

# Para iniciar el servidor, usa el comando: uvicorn app:app --reload

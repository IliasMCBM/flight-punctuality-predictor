from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler
from sklearn.impute import KNNImputer
from sklearn.metrics import classification_report
from joblib import parallel_backend
import time
import pandas as pd
import xgboost as xgb
df=pd.read_csv('C:/Users/ilias/Documents/AMD/Poryecto/combined_2023.csv')
# Importar la función para el manejo de desbalance de clases en XGBoost
from xgboost import XGBClassifier
df = df.dropna()
# Cargar los datos y definir X e y
X = df.drop(columns=['ARR_DEL15'])
y = df['ARR_DEL15']

# Semilla para reproducibilidad
seed = 123

# Dividir los datos en entrenamiento y prueba con semilla y estratificación
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed, stratify=y)

# Definir las transformaciones para datos numéricos y categóricos
numeric_features = X.select_dtypes(include=['float64', 'int64']).columns
categorical_features = X.select_dtypes(include=['object']).columns

numeric_transformer = Pipeline(steps=[
    ('imputer', KNNImputer(n_neighbors=5, weights='uniform')),
    ('scaler', RobustScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

# Combinar las transformaciones
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Definir el modelo XGBoost con manejo de desbalance de clases
model = XGBClassifier(random_state=seed, n_estimators=15, max_depth=13, booster='gbtree', scale_pos_weight=(len(y) - y.sum()) / y.sum())

# Definir el pipeline que incluye la transformación y el modelo
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', model)])

# Entrenar el modelo
start_training_time = time.time()  # Iniciar el temporizador para el entrenamiento
pipeline.fit(X_train, y_train)
end_training_time = time.time()  # Finalizar el temporizador para el entrenamiento

# Predecir en el conjunto de prueba
start_prediction_time = time.time()  # Iniciar el temporizador para la predicción
y_pred = pipeline.predict(X_test)
end_prediction_time = time.time()  # Finalizar el temporizador para la predicción

# Mostrar métricas de evaluación
print(classification_report(y_test, y_pred))

# Tiempo total de entrenamiento y predicción
print(f"Tiempo total de entrenamiento: {end_training_time - start_training_time} segundos")
print(f"Tiempo total de predicción: {end_prediction_time - start_prediction_time} segundos")


import joblib

# Ajustar el pipeline con los datos de entrenamiento
pipeline.fit(X_train, y_train)

# Guardar el modelo usando joblib
joblib_filename = "xgboost_model.joblib"
joblib.dump(pipeline, joblib_filename)
print(f"Modelo XGBoost guardado en {joblib_filename}")
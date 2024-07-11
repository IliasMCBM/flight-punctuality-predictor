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
df = pd.read_csv('combined_2023.csv')
# Import the function for handling class imbalance in XGBoost
from xgboost import XGBClassifier
df = df.dropna()
# Load the data and define X and y
X = df.drop(columns=['ARR_DEL15'])
y = df['ARR_DEL15']

# Seed for reproducibility
seed = 123

# Split the data into training and testing sets with seed and stratification
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed, stratify=y)

# Define the transformations for numeric and categorical data
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

# Combine the transformations
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Define the XGBoost model with class imbalance handling
model = XGBClassifier(random_state=seed, n_estimators=15, max_depth=13, booster='gbtree', scale_pos_weight=(len(y) - y.sum()) / y.sum())

# Define the pipeline that includes the transformation and the model
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', model)])

# Train the model
start_training_time = time.time()  # Start the timer for training
pipeline.fit(X_train, y_train)
end_training_time = time.time()  # End the timer for training

# Predict on the test set
start_prediction_time = time.time()  # Start the timer for prediction
y_pred = pipeline.predict(X_test)
end_prediction_time = time.time()  # End the timer for prediction

# Display evaluation metrics
print(classification_report(y_test, y_pred))

# Total training and prediction time
print(f"Total training time: {end_training_time - start_training_time} seconds")
print(f"Total prediction time: {end_prediction_time - start_prediction_time} seconds")


import joblib

# Fit the pipeline with the training data
pipeline.fit(X_train, y_train)

# Save the model using joblib
joblib_filename = "xgboost_model.joblib"
joblib.dump(pipeline, joblib_filename)
print(f"XGBoost model saved as {joblib_filename}")

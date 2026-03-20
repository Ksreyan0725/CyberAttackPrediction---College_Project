import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Get the base directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
DATASET_PATH = os.path.join(BASE_DIR, "Dataset", "kdd_train.csv")
MODEL_OUTPUT_PATH = os.path.join(MODEL_DIR, "trained_rf_model.pkl")

# Ensure model directory exists
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

print(f"Training model using data from: {DATASET_PATH}")

# Load dataset
if not os.path.exists(DATASET_PATH):
    print(f"ERROR: Dataset not found at {DATASET_PATH}")
    exit(1)

dataset = pd.read_csv(DATASET_PATH, nrows=20000)
labels = np.unique(dataset['labels']).ravel()

# Preprocessing
label_encoder = []
columns = dataset.columns
for col in dataset.columns:
    if not pd.api.types.is_numeric_dtype(dataset[col]):
        le = LabelEncoder()
        dataset[col] = le.fit_transform(dataset[col].astype(str))
        label_encoder.append([col, le])

dataset.fillna(0, inplace=True)
Y = dataset['labels'].values.ravel()
Y = Y.astype('int')
dataset.drop(['labels'], axis=1, inplace=True)

# Normalization
scaler = StandardScaler()
X = scaler.fit_transform(dataset.values)

# Training
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
rf_cls = RandomForestClassifier(n_estimators=100, random_state=42)
rf_cls.fit(X_train, y_train)

# Save everything
model_data = {
    'rf_model': rf_cls,
    'scaler': scaler,
    'labels': labels,
    'label_encoder': label_encoder,
    'feature_columns': dataset.columns.tolist()
}

with open(MODEL_OUTPUT_PATH, "wb") as f:
    pickle.dump(model_data, f)

print(f"Model, scaler, and encoders saved to {MODEL_OUTPUT_PATH}")

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Ensure model directory exists
if not os.path.exists("model"):
    os.makedirs("model")

print("Training model...")

# Load dataset
dataset = pd.read_csv("Dataset/kdd_train.csv", nrows=20000)
labels = np.unique(dataset['labels']).ravel()

# Preprocessing
label_encoder = []
columns = dataset.columns
types = dataset.dtypes.values
for j in range(len(types)):
    name = types[j]
    if name == 'object':
        le = LabelEncoder()
        dataset[columns[j]] = pd.Series(le.fit_transform(dataset[columns[j]].astype(str)))
        label_encoder.append([columns[j], le])

dataset.fillna(0, inplace=True)
Y = dataset['labels'].ravel()
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

with open("model/trained_rf_model.pkl", "wb") as f:
    pickle.dump(model_data, f)

print("Model, scaler, and encoders saved to model/trained_rf_model.pkl")

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def run_training():
    # Get the base directory where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(base_dir, "model")
    dataset_path = os.path.join(base_dir, "Dataset", "kdd_train.csv")
    model_output_path = os.path.join(model_dir, "trained_rf_model.pkl")

    # Ensure model directory exists
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    print(f"Training model using data from: {dataset_path}")

    # Load dataset
    if not os.path.exists(dataset_path):
        return {"status": "error", "message": f"Dataset not found at {dataset_path}"}

    try:
        dataset = pd.read_csv(dataset_path, nrows=20000)
        labels_list = np.unique(dataset['labels']).ravel()

        # Preprocessing
        label_encoder = []
        for col in dataset.columns:
            if not pd.api.types.is_numeric_dtype(dataset[col]):
                le = LabelEncoder()
                dataset[col] = le.fit_transform(dataset[col].astype(str))
                label_encoder.append([col, le])

        dataset.fillna(0, inplace=True)
        Y = dataset['labels'].values.ravel().astype('int')
        dataset.drop(['labels'], axis=1, inplace=True)

        # Normalization
        scaler = StandardScaler()
        X = scaler.fit_transform(dataset.values)

        # Training
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        rf_cls = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_cls.fit(X_train, y_train)

        # Evaluation
        accuracy = rf_cls.score(X_test, y_test)

        # Save everything
        model_data = {
            'rf_model': rf_cls,
            'scaler': scaler,
            'labels': labels_list,
            'label_encoder': label_encoder,
            'feature_columns': dataset.columns.tolist()
        }

        with open(model_output_path, "wb") as f:
            pickle.dump(model_data, f)

        return {
            "status": "success",
            "accuracy": round(accuracy * 100, 2),
            "model_path": model_output_path,
            "classes": labels_list.tolist()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    result = run_training()
    print(result)

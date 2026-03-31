import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def run_training(dataset_path=None):
    # Get the base directory where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(base_dir, "model")
    
    # Use default path if none provided
    if not dataset_path:
        dataset_path = os.path.join(base_dir, "Dataset", "kdd_train.csv")
    
    model_output_path = os.path.join(model_dir, "trained_rf_model.pkl")

    # 🛡️ Layer 1: System Permissions & Directory
    if not os.path.exists(model_dir):
        try:
            os.makedirs(model_dir)
        except Exception as e:
            return {"status": "error", "message": f"Could not create model directory: {str(e)}"}
    
    if not os.access(model_dir, os.W_OK):
        return {"status": "error", "message": "Model directory is not writable. Please check permissions."}

    print(f"Training model using data from: {dataset_path}")

    # 🛡️ Layer 2: Dataset Integrity Check
    if not os.path.exists(dataset_path):
        return {"status": "error", "message": f"Dataset file not found: {os.path.basename(dataset_path)}"}

    try:
        # Load sample to verify structure
        dataset = pd.read_csv(dataset_path, nrows=20000)
        
        if dataset.empty:
            return {"status": "error", "message": "The provided dataset is empty."}
            
        if 'labels' not in dataset.columns:
            return {"status": "error", "message": "Invalid Dataset: Missing required 'labels' column for training."}

        labels_list = np.unique(dataset['labels']).ravel()

        # 🛡️ Layer 3: Robust Preprocessing
        label_encoder = []
        for col in dataset.columns:
            try:
                if not pd.api.types.is_numeric_dtype(dataset[col]):
                    le = LabelEncoder()
                    dataset[col] = le.fit_transform(dataset[col].astype(str))
                    label_encoder.append([col, le])
            except Exception as e:
                return {"status": "error", "message": f"Character encoding failed on column '{col}': {str(e)}"}

        dataset.fillna(0, inplace=True)
        
        # Verify classes are valid for classification
        Y = dataset['labels'].values.ravel().astype('int')
        if len(np.unique(Y)) < 2:
             return {"status": "error", "message": "Insufficient data: Model requires at least 2 distinct classes to train."}
             
        dataset.drop(['labels'], axis=1, inplace=True)

        # 🛡️ Layer 4: Mathematical Normalization
        scaler = StandardScaler()
        try:
            X = scaler.fit_transform(dataset.values)
        except Exception as e:
            return {"status": "error", "message": f"Data normalization failed: {str(e)}. Ensure your dataset contains numeric features."}

        # Training
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        rf_cls = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_cls.fit(X_train, y_train)

        # Evaluation
        accuracy = rf_cls.score(X_test, y_test)

        # Save everything (Atomic-ish write)
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
            "classes": labels_list.tolist(),
            "dataset_used": os.path.basename(dataset_path)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    result = run_training()
    
    print("\n" + "="*60)
    print("🛡️  CYBERSHIELD AI: MODEL TRAINING REPORT")
    print("="*60)
    
    if result.get('status') == 'success':
        print(f"✅ STATUS:    SUCCESS")
        print(f"🎯 ACCURACY:  {result.get('accuracy')}%")
        print(f"💾 SAVED TO:  {result.get('model_path')}")
        
        classes = result.get('classes', [])
        print(f"\n🚀 DETECTABLE ATTACK CLASSES ({len(classes)}):")
        print("-" * 60)
        
        # Print classes in a 3-column grid for readability
        for i in range(0, len(classes), 3):
            row = classes[i:i+3]
            formatted_row = "  ".join(f"• {c:<18}" for c in row)
            print(formatted_row)
    else:
        print(f"❌ STATUS:    FAILED")
        print(f"⚠️ ERROR:     {result.get('message')}")
        
    print("="*60 + "\n")
    

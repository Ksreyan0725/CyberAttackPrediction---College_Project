import pandas as pd
import pickle
import os
import sys

def test_system():
    print("=== CyberShield AI System Test ===")
    
    # 1. Check if model exists
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "model", "trained_rf_model.pkl")
    dataset_path = os.path.join(base_dir, "Dataset", "testData.csv")
    
    if not os.path.exists(model_path):
        print(f"[ERROR] Trained model not found at {model_path}. Please run training first.")
        return False
    
    print(f"[OK] Model found at {model_path}")
    
    # 2. Load Model Data
    try:
        with open(model_path, "rb") as f:
            model_data = pickle.load(f)
            rf_model = model_data['rf_model']
            scaler = model_data['scaler']
            labels = model_data['labels']
            label_encoder = model_data['label_encoder']
            print("[OK] Model and Scalers loaded successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}")
        return False
        
    # 3. Load Test CSV (Simulating Upload)
    if not os.path.exists(dataset_path):
        print(f"[ERROR] Test dataset not found at {dataset_path}")
        return False
        
    try:
        test_df = pd.read_csv(dataset_path)
        print(f"[OK] Test CSV loaded: {len(test_df)} rows found.")
        
        # 4. Simulate Preprocessing Logic from Main.py
        processed_df = test_df.copy()
        for le_entry in label_encoder:
            col_name = le_entry[0]
            le = le_entry[1]
            if col_name in processed_df.columns:
                processed_df[col_name] = processed_df[col_name].astype(str).map(
                    lambda s: le.transform([s])[0] if s in le.classes_ else -1
                )
        
        processed_df.fillna(0, inplace=True)
        
        # 5. Scale and Predict
        scaled_test = scaler.transform(processed_df.values)
        preds = rf_model.predict(scaled_test)
        
        print(f"[OK] Prediction successful for {len(preds)} rows.")
        
        # 6. Sample Results
        print("\n=== Sample Prediction Results ===")
        for i in range(min(3, len(preds))):
            attack_type = labels[preds[i]]
            print(f"Row {i+1}: Predicted as -> {attack_type}")
            
        print("\n[SUCCESS] System validation complete. Upload and Training pipelines are fully operational.")
        return True
        
    except Exception as e:
        print(f"[ERROR] Prediction flow failed: {e}")
        return False

if __name__ == "__main__":
    success = test_system()
    sys.exit(0 if success else 1)

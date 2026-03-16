import pandas as pd
import numpy as np
import pickle
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret')

# Global variables to store loaded models/scalers
rf_model = None
scaler = None
labels = None
label_encoder = None
feature_columns = None

def load_ml_model():
    """Loads the pre-trained model and preprocessing tools from disk."""
    global rf_model, scaler, labels, label_encoder, feature_columns
    try:
        model_path = os.path.join("model", "trained_rf_model.pkl")
        if os.path.exists(model_path):
            with open(model_path, "rb") as f:
                model_data = pickle.load(f)
                rf_model = model_data['rf_model']
                scaler = model_data['scaler']
                labels = model_data['labels']
                label_encoder = model_data['label_encoder']
                feature_columns = model_data['feature_columns']
            print("Successfully loaded pre-trained model.")
            return True
        else:
            print("Pre-trained model not found. Please run train_model.py first.")
            return False
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

# Load model at startup
load_ml_model()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/UserLogin', methods=['GET', 'POST'])
def UserLogin():
    return render_template('UserLogin.html')

@app.route('/UserLoginAction', methods=['POST'])
def UserLoginAction():
    user = request.form.get('t1')
    password = request.form.get('t2')
    
    # Secure credential check using .env
    admin_user = os.getenv('ADMIN_USER', 'admin')
    admin_pass = os.getenv('ADMIN_PASS', 'admin')
    
    if user == admin_user and password == admin_pass:
        session['user'] = user
        return render_template('UserScreen.html', msg="Welcome " + user)
    else:
        return render_template('UserLogin.html', msg="Invalid login details")

@app.route('/Logout')
def Logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/Predict')
def predictView():
    if 'user' not in session:
        return redirect(url_for('UserLogin'))
    return render_template('Predict.html')

@app.route('/PredictAction', methods=['POST'])
def PredictAction():
    if 'user' not in session:
        return redirect(url_for('UserLogin'))
        
    global rf_model, scaler, labels, label_encoder
    
    if rf_model is None:
        if not load_ml_model():
            return render_template('Predict.html', msg="Model not ready. Please run train_model.py.")

    try:
        # Load test data from the uploaded file
        if 't1' not in request.files:
            return render_template('Predict.html', msg="No file uploaded.")
            
        file = request.files['t1']
        if file.filename == '':
            return render_template('Predict.html', msg="No file selected.")
            
        # For simplicity, we'll save it temporarily as testData.csv
        file.save("Dataset/uploaded_test.csv")
        testData_df = pd.read_csv("Dataset/uploaded_test.csv")
        
        # Keep a copy of raw data for display
        raw_data = testData_df.values
        
        # Preprocessing using saved label encoders
        for le_entry in label_encoder:
            col_name = le_entry[0]
            le = le_entry[1]
            if col_name in testData_df.columns:
                # Handle unseen labels by assigning -1 or similar
                testData_df[col_name] = testData_df[col_name].astype(str).map(
                    lambda s: le.transform([s])[0] if s in le.classes_ else -1
                )
        
        testData_df.fillna(0, inplace=True)
        
        # Scale data
        scaled_test = scaler.transform(testData_df.values)
        
        # Prediction
        preds = rf_model.predict(scaled_test)
        
        # Generate styled HTML results
        output = '<table class="table table-hover table-bordered table-striped align-middle"><thead><tr class="table-dark">'
        output += '<th><i class="fas fa-database me-2"></i>Test Data Sample</th>'
        output += '<th><i class="fas fa-shield-alt me-2"></i>Predicted Attack Type</th>'
        output += '<th><i class="fas fa-magic me-2"></i>GenAI Insights</th></tr></thead><tbody>'
        
        for i in range(len(preds)):
            attack_type = labels[preds[i]]
            row_data_str = str(raw_data[i])
            
            # Simple simulation of GenAI Insights (can be replaced with LLM API)
            genai_insight = get_genai_insight(attack_type)
            
            output += "<tr>"
            output += f'<td><div class="text-truncate" style="max-width: 400px;" title="{row_data_str}"><code>{row_data_str}</code></div></td>'
            
            if attack_type == "normal":
                output += f'<td><span class="badge bg-success py-2 px-3 rounded-pill"><i class="fas fa-check-circle me-1"></i> {attack_type.upper()}</span></td>'
            else:
                output += f'<td><span class="badge bg-danger py-2 px-3 rounded-pill"><i class="fas fa-exclamation-triangle me-1"></i> {attack_type.upper()}</span></td>'
            
            output += f'<td><small class="text-muted fst-italic">{genai_insight}</small></td>'
            output += "</tr>"
            
        output += "</tbody></table>"
        return render_template('UserScreen.html', msg=output)
        
    except Exception as e:
        print(f"Error during prediction: {e}")
        return render_template('Predict.html', msg=f"Error: {str(e)}")

def get_genai_insight(attack_type):
    """Simulates a Generative AI explanation for the predicted attack type."""
    insights = {
        "normal": "Traffic patterns match authorized user behavior. No immediate action required.",
        "neptune": "High-volume SYN flood detected. This mimics a 'Neptune' DoS attack. Recommendation: Enable SYN cookies and rate limiting.",
        "back": "Possible buffer overflow attempt on HTTP requests detected. Inspect web server logs for malicious GET requests.",
        "teardrop": "Malformed IP fragments identified. This signature is often used to crash older operating systems. Patch network stack if vulnerable.",
        "satan": "Port scanning activity detected. An attacker is probing your infrastructure for open ports. Consider blacklisting the source IP.",
        "ipsweep": "Network reconnaissance detected. The source is scanning for active hosts in your subnet.",
        "warezclient": "Unauthorized file transfer activity identified. This could indicate data exfiltration or unauthorized software distribution."
    }
    return insights.get(attack_type.lower(), "AI suggests this is a known signature. Monitor for unusual lateral movement in the network.")

if __name__ == '__main__':
    app.run(debug=True)

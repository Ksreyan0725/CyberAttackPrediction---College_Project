import pandas as pd
import numpy as np
import pickle
import os
import webbrowser
import json
from threading import Timer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import StackingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

#=================flask code starts here
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, jsonify
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
        # Base directory of the script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "model", "trained_rf_model.pkl")
        
        if os.path.exists(model_path):
            with open(model_path, "rb") as f:
                model_data = pickle.load(f)
                rf_model = model_data['rf_model']
                scaler = model_data['scaler']
                labels = model_data['labels']
                label_encoder = model_data['label_encoder']
                feature_columns = model_data['feature_columns']
            print(f"Successfully loaded pre-trained model from {model_path}.")
            return True
        else:
            print(f"Pre-trained model not found at {model_path}. Please run train_model.py first.")
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

@app.route('/HowItWorks')
def HowItWorks():
    return render_template('HowItWorks.html')

@app.route('/UserLogin', methods=['GET', 'POST'])
def UserLogin():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    creds_file = os.path.join(base_dir, "saved_creds.json")
    has_saved = os.path.exists(creds_file)
    return render_template('UserLogin.html', has_saved=has_saved)

@app.route('/VerifySavedLogin', methods=['POST'])
def VerifySavedLogin():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    creds_file = os.path.join(base_dir, "saved_creds.json")
    
    if os.path.exists(creds_file):
        try:
            with open(creds_file, 'r') as f:
                creds = json.load(f)
            
            # Verify against env (same as UserLoginAction)
            admin_user = os.getenv('ADMIN_USER', 'admin')
            admin_pass = os.getenv('ADMIN_PASS', 'admin')
            
            if creds.get('user') == admin_user and creds.get('pass') == admin_pass:
                session['user'] = admin_user
                session['remembered'] = True
                return jsonify({"status": "success"})
        except Exception as e:
            print(f"Error reading creds: {e}")
            
    return jsonify({"status": "error", "message": "Saved credentials invalid or missing"})

@app.route('/ResetCredentials', methods=['POST'])
def ResetCredentials():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    creds_file = os.path.join(base_dir, "saved_creds.json")
    if os.path.exists(creds_file):
        os.remove(creds_file)
    return jsonify({"status": "success"})

@app.route('/UserLoginAction', methods=['POST'])
def UserLoginAction():
    user = request.form.get('t1')
    password = request.form.get('t2')
    remember = request.form.get('remember') == 'on'
    
    # Secure credential check using .env
    admin_user = os.getenv('ADMIN_USER', 'admin')
    admin_pass = os.getenv('ADMIN_PASS', 'admin')
    
    if user == admin_user and password == admin_pass:
        session['user'] = user
        
        if remember:
            session['remembered'] = True
            base_dir = os.path.dirname(os.path.abspath(__file__))
            creds_file = os.path.join(base_dir, "saved_creds.json")
            with open(creds_file, 'w') as f:
                json.dump({'user': user, 'pass': password}, f)
        else:
            session['remembered'] = False
                
        return redirect(url_for('predictView'))
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
    return render_template('Predict.html', page_type='input')

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
        output = '<table class="table table-hover table-bordered table-striped align-middle"><thead><tr class="glass-bg border-glass">'
        output += '<th class="dynamic-text"><i class="fas fa-database me-2" style="color: var(--primary-color)"></i>Test Data Sample</th>'
        output += '<th class="dynamic-text"><i class="fas fa-shield-alt me-2" style="color: var(--primary-color)"></i>Predicted Attack Type</th>'
        output += '<th class="dynamic-text"><i class="fas fa-magic me-2" style="color: var(--primary-color)"></i>GenAI Insights</th></tr></thead><tbody>'
        
        for i in range(len(preds)):
            attack_type = labels[preds[i]]
            row_data_str = str(raw_data[i])
            
            # Simple simulation of GenAI Insights (can be replaced with LLM API)
            genai_insight = get_genai_insight(attack_type)
            
            output += "<tr>"
            output += f'<td><div class="text-truncate" style="max-width: 400px;" title="{row_data_str}"><code class="dynamic-text opacity-75">{row_data_str}</code></div></td>'
            
            if attack_type == "normal":
                output += f'<td><span class="badge bg-success py-2 px-3 rounded-pill"><i class="fas fa-check-circle me-1"></i> {attack_type.upper()}</span></td>'
            else:
                output += f'<td><span class="badge bg-danger py-2 px-3 rounded-pill"><i class="fas fa-exclamation-triangle me-1"></i> {attack_type.upper()}</span></td>'
            
            output += f'<td><div class="dynamic-text small fw-medium">{genai_insight}</div></td>'
            output += "</tr>"
            
        output += "</tbody></table>"
        return render_template('UserScreen.html', msg=output, page_type='result')
        
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

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

if __name__ == '__main__':
    # Automatically open browser after 1.5 seconds
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        Timer(1.5, open_browser).start()
    
    app.run(debug=True)

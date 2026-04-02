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
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from train_model import run_training
import markdown2
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter
import nbformat
from nbconvert import HTMLExporter

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
    # Allow manual reset via query param or button
    if request.args.get('reset') == 'true':
        session.pop('last_result', None)
        session.pop('last_page_type', None)
        return redirect(url_for('index'))

    # If there is a last result in session, restore it automatically for soft navigation
    if 'last_result' in session and 'last_page_type' in session:
        return render_template('UserScreen.html', 
                               msg=session['last_result'], 
                               page_type=session['last_page_type'])
    return render_template('index.html')

@app.route('/HowItWorks')
def HowItWorks():
    return render_template('HowItWorks.html')

@app.route('/Predict')
@app.route('/PredictView')
def predictView():
    if 'user' not in session:
        return redirect(url_for('UserLogin'))
    
    # Check if model is actually ready before allowing prediction
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "model", "trained_rf_model.pkl")
    if not os.path.exists(model_path):
        flash("Model not found. Please train the model before running predictions.", "warning")
        return redirect(url_for('train_view'))
    
    # If reset is requested, clear the last result
    if request.args.get('reset') == 'true':
        session.pop('last_result', None)
        session.pop('last_page_type', None)
        return redirect(url_for('predictView'))
        
    # Allow the UI to know if a result already exists in this session
    last_result = session.get('last_result')
    return render_template('Predict.html', page_type='input', last_result=last_result)

@app.route('/api/clear-session', methods=['POST'])
def clear_session():
    """API endpoint to clear specific session results for system reset."""
    if not session.get('user'):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
        
    session.pop('last_result', None)
    session.pop('last_page_type', None)
    return jsonify({"status": "success", "message": "Session data cleared successfully"})

# --- Security & User Management ---
USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")

def load_users():
    # ULTIMATE ADMIN BYPASS (Hardcoded)
    if not os.path.exists(USERS_FILE):
        users = {
            "admin": {
                "username": "admin",
                "password": generate_password_hash("admin"),
                "role": "admin"
            }
        }
        save_users(users)
        return users
    
    try:
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
            # Ensure hardcoded admin always exists with original power if deleted
            if "admin" not in users:
                users["admin"] = {
                    "username": "admin",
                    "password": generate_password_hash("admin"),
                    "role": "admin"
                }
                save_users(users)
            return users
    except:
        return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

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
            
            # ULTIMATE ADMIN BYPASS
            if creds.get('user') == "admin" and creds.get('pass') == "admin":
                session['user'] = "admin"
                session['is_ultimate'] = True
                session['remembered'] = True
                return jsonify({"status": "success"})
            
            users = load_users()
            user_data = users.get(creds.get('user'))
            
            # Verify saved hash if present, otherwise fallback to plain check (for migration)
            if user_data and check_password_hash(user_data['password'], creds.get('pass')):
                session['user'] = user_data['username']
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
    username = request.form.get('t1')
    password = request.form.get('t2')
    remember = request.form.get('remember') == 'on'
    
    # ULTIMATE BYPASS CHECK
    if username == "admin" and password == "admin":
        session['user'] = "admin"
        session['is_ultimate'] = True
        if remember:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(base_dir, "saved_creds.json"), 'w') as f:
                json.dump({"user": "admin", "pass": "admin"}, f)
            session['remembered'] = True
        return jsonify({"status": "success", "message": "Ultimate Admin access granted!", "redirect": url_for('train_view')})

    users = load_users()
    user_data = users.get(username)
    
    if user_data and check_password_hash(user_data['password'], password):
        session['user'] = user_data['username']
        
        # Save credentials locally if "Remember Me" is checked
        if remember:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(base_dir, "saved_creds.json"), 'w') as f:
                json.dump({"user": username, "pass": password}, f)
            session['remembered'] = True
        
        return jsonify({"status": "success", "message": f"Welcome back, {username}!", "redirect": url_for('train_view')})
    else:
        return jsonify({"status": "error", "message": "Invalid username or password"}), 401

@app.route('/Signup')
def Signup():
    return render_template('Signup.html')

@app.route('/SignupAction', methods=['POST'])
def SignupAction():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    if password != confirm_password:
        flash("Passwords do not match!", "danger")
        return redirect(url_for('Signup'))
        
    users = load_users()
    if username in users:
        flash("Username already exists!", "danger")
        return redirect(url_for('Signup'))
        
    users[username] = {
        "username": username,
        "password": generate_password_hash(password),
        "role": "user"
    }
    save_users(users)
    flash("Account created! Please login.", "success")
    return redirect(url_for('UserLogin'))

@app.route('/Account')
def Account():
    if 'user' not in session:
        return redirect(url_for('UserLogin'))
    users = load_users()
    user_data = users.get(session['user'])
    return render_template('AccountSettings.html', user_data=user_data)

@app.route('/UpdateAccountAction', methods=['POST'])
def UpdateAccountAction():
    if 'user' not in session:
        return redirect(url_for('UserLogin'))
        
    new_username = request.form.get('username')
    new_password = request.form.get('password')
    old_username = session['user']
    
    users = load_users()
    if old_username not in users:
        # Check for ultimate admin bypass
        if old_username == "admin" and session.get('is_ultimate'):
            # Ultimate admin can update themselves too (stored in file if they want)
            user_data = {"username": "admin", "password": generate_password_hash("admin"), "role": "admin"}
        else:
            flash("User session expired. Please login again.", "danger")
            return redirect(url_for('UserLogin'))
    else:
        user_data = users.pop(old_username)
    
    # Update username if changed and not taken
    if new_username != old_username:
        if new_username in users:
            users[old_username] = user_data # Restore
            flash("New username already taken!", "danger")
            return redirect(url_for('Account'))
        user_data['username'] = new_username
        session['user'] = new_username
        
    # Update password if provided
    if new_password:
        user_data['password'] = generate_password_hash(new_password)
        
    users[user_data['username']] = user_data
    save_users(users)
    flash("Profile updated successfully!", "success")
    return redirect(url_for('Account'))

@app.route('/AdminGetUsers')
def AdminGetUsers():
    """Returns a list of all users for the dashboard."""
    if 'user' not in session or (session.get('user') != 'admin' and not session.get('is_ultimate')):
        return jsonify({"status": "error", "message": "Unauthorized"}), 403
    
    users = load_users()
    user_list = []
    for uname, data in users.items():
        user_list.append({
            "username": uname,
            "role": data.get('role', 'user')
        })
    return jsonify(user_list)

@app.route('/AdminDeleteUser', methods=['POST'])
def AdminDeleteUser():
    """Deletes a user account (Admin only)."""
    if 'user' not in session or (session.get('user') != 'admin' and not session.get('is_ultimate')):
        return jsonify({"status": "error", "message": "Unauthorized"}), 403
    
    target_user = request.json.get('username')
    if target_user == "admin" or target_user == session['user']:
        return jsonify({"status": "error", "message": "Cannot delete root admin or current session"}), 400
        
    users = load_users()
    if target_user in users:
        del users[target_user]
        save_users(users)
        return jsonify({"status": "success", "message": f"User {target_user} deleted"})
    return jsonify({"status": "error", "message": "User not found"}), 404

@app.route('/AdminResetPassword', methods=['POST'])
def AdminResetPassword():
    """Allows an administrator to reset a user's password."""
    if 'user' not in session or (session.get('user') != 'admin' and not session.get('is_ultimate')):
        return jsonify({"status": "error", "message": "Unauthorized"}), 403
    
    data = request.json
    target_user = data.get('username')
    new_password = data.get('password')
    
    if not target_user or not new_password:
        return jsonify({"status": "error", "message": "Username and new password are required"}), 400
        
    if target_user == "admin" and not session.get('is_ultimate'):
         return jsonify({"status": "error", "message": "Only the developer can reset the root account"}), 400

    users = load_users()
    if target_user in users:
        users[target_user]['password'] = generate_password_hash(new_password)
        save_users(users)
        return jsonify({"status": "success", "message": f"Credentials for {target_user} have been updated"})
    
    return jsonify({"status": "error", "message": "User not found"}), 404

@app.route('/Logout')
def Logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/PredictAction', methods=['POST'])
def PredictAction():
    if 'user' not in session:
        return redirect(url_for('UserLogin'))
        
    global rf_model, scaler, labels, label_encoder
    
    if rf_model is None:
        if not load_ml_model():
            flash("Model not ready. Please run the training process first.", "warning")
            return redirect(url_for('train_view'))

    try:
        # Load test data from the uploaded file
        if 't1' not in request.files:
            flash("No file was uploaded. Please select a CSV file.", "error")
            return redirect(url_for('predictView'))
            
        file = request.files['t1']
        if file.filename == '':
            flash("No file was selected. Please try again.", "error")
            return redirect(url_for('predictView'))
            
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
        
        # Generate styled HTML results with improved contrast
        output = '<table class="table table-hover table-bordered table-striped align-middle mb-0">'
        output += '<thead><tr class="glass-bg border-glass">'
        output += '<th class="dynamic-text fw-bold py-3"><i class="fas fa-database me-2 text-info"></i>Data Sample</th>'
        output += '<th class="dynamic-text fw-bold py-3 text-center"><i class="fas fa-shield-alt me-2 text-primary"></i>Detection Status</th>'
        output += '<th class="dynamic-text fw-bold py-3"><i class="fas fa-magic me-2 text-warning"></i>GenAI Explanation</th></tr></thead><tbody>'
        
        for i in range(len(preds)):
            attack_type = labels[preds[i]]
            row_data_str = str(raw_data[i])
            
            # Simple simulation of GenAI Insights
            genai_insight = get_genai_insight(attack_type)
            
            output += "<tr>"
            # Row Data (Left)
            output += f'<td><div class="text-truncate" style="max-width: 380px;" title="{row_data_str}"><code class="dynamic-text fw-medium">{row_data_str}</code></div></td>'
            
            # Status Badge (Middle)
            is_normal = "normal" in attack_type.lower().strip()
            if is_normal:
                output += f'<td class="text-center"><span class="badge bg-success py-2 px-3 rounded-pill shadow-sm"><i class="fas fa-check-circle me-1"></i> {attack_type.upper()}</span></td>'
            else:
                output += f'<td class="text-center"><span class="badge bg-danger py-2 px-3 rounded-pill shadow-sm"><i class="fas fa-skull-crossbones me-1"></i> {attack_type.upper()}</span></td>'
            
            # GenAI Insight (Right)
            output += f'<td><div class="dynamic-text small fw-medium text-wrap">{genai_insight}</div></td>'
            output += "</tr>"
            
        output += "</tbody></table>"
        
        # Save to session for persistence across navigation
        session['last_result'] = output
        session['last_page_type'] = 'result'
        
        return render_template('UserScreen.html', msg=output, page_type='result')
        
    except Exception as e:
        print(f"Error during prediction: {e}")
        flash(f"Analysis failed: {str(e)}", "error")
        return redirect(url_for('predictView'))

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
    webbrowser.open_new("http://127.0.0.1:2026/")

@app.route('/documentation')
def documentation():
    if 'user' not in session:
        return redirect(url_for('UserLogin'))
    return render_template('project overview.html')

@app.route('/explorer')
def explorer():
    if 'user' not in session:
        return redirect(url_for('UserLogin'))
        
    doc_path = request.args.get('doc', 'README.md')
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Root
    
    # Simple security check to prevent directory traversal
    if '..' in doc_path or doc_path.startswith('/'):
        return render_template('documentation.html', error="Invalid path")
        
    full_path = os.path.join(base_dir, doc_path)
    if not os.path.exists(full_path):
        return render_template('documentation.html', error=f"File not found: {doc_path}")
        
    try:
        ext = os.path.splitext(doc_path)[1].lower()
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if ext == '.md':
            html_content = markdown2.markdown(content, extras=["tables", "fenced-code-blocks", "toc", "header-ids"])
            doc_type = 'markdown'
        elif ext == '.ipynb':
            nb = nbformat.reads(content, as_version=4)
            html_exporter = HTMLExporter()
            html_exporter.template_name = 'basic' # Simple clean output
            (html_content, resources) = html_exporter.from_notebook_node(nb)
            doc_type = 'notebook'
        elif ext in ['.py', '.bat', '.ps1', '.json', '.html', '.css', '.js']:
            lexer = get_lexer_for_filename(full_path)
            formatter = HtmlFormatter(style='monokai', full=False, cssclass="highlight")
            html_content = highlight(content, lexer, formatter)
            doc_type = 'code'
            # Add simple wrapper for code styling if needed
            html_content = f'<style>{formatter.get_style_defs(".highlight")}</style>{html_content}'
        else:
            # Plain text
            html_content = f'<pre style="white-space: pre-wrap; word-wrap: break-word;">{content}</pre>'
            doc_type = 'text'
            
        return render_template('documentation.html', md_content=html_content, current_doc=doc_path, doc_type=doc_type)
        
    except Exception as e:
        return render_template('documentation.html', error=f"Rendering error: {str(e)}")

@app.route('/Train')
def train_view():
    if 'user' not in session:
        return redirect(url_for('UserLogin'))
    
    # Check if a model has already been trained using the standardized path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "model", "trained_rf_model.pkl")
    model_ready = os.path.exists(model_path)
    
    train_result = session.get('train_result')
    return render_template('Train.html', page_type='train', model_ready=model_ready, train_result=train_result)

@app.route('/DownloadSample')
def DownloadSample():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    dataset_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Dataset")
    return send_from_directory(dataset_dir, "sample_train.csv", as_attachment=True)

@app.route('/TrainAction', methods=['POST'])
def TrainAction():
    if 'user' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    # Check if a custom file was uploaded
    custom_path = None
    if 'training_data' in request.files:
        file = request.files['training_data']
        if file.filename != '':
            # Ensure Dataset directory exists
            base_dir = os.path.dirname(os.path.abspath(__file__))
            dataset_dir = os.path.join(base_dir, "Dataset")
            if not os.path.exists(dataset_dir):
                os.makedirs(dataset_dir)
            
            custom_path = os.path.join(dataset_dir, "custom_train.csv")
            try:
                file.save(custom_path)
            except Exception as e:
                return jsonify({"status": "error", "message": f"Failed to save training file: {str(e)}"})
    
    # Call training with optional path
    result = run_training(dataset_path=custom_path)
    
    # If training was successful, reload the model in memory and persist in session
    if result.get('status') == 'success':
        load_ml_model()
        session['train_result'] = result
        
    return jsonify(result)

if __name__ == '__main__':
    # Automatically open browser after 1.5 seconds
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        Timer(1.5, open_browser).start()
    
    app.run(debug=True, port=2026)

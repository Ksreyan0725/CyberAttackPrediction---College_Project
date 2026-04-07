import pandas as pd
import numpy as np
import joblib
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
import secrets
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
import logging

# Silence repetitive Heartbeat logs for a cleaner terminal experience
class HeartbeatFilter(logging.Filter):
    def filter(self, record):
        # Exclude any log record containing the heartbeat URI
        return "/api/heartbeat" not in record.getMessage()

log = logging.getLogger('werkzeug')
log.addFilter(HeartbeatFilter())

# Load environment variables
load_dotenv()

app = Flask(__name__, static_url_path='')
# Use a derived secret key for session integrity; fallback to a generated secret if environment is missing
app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32) if not os.getenv('FLASK_SECRET_KEY') else os.getenv('FLASK_SECRET_KEY'))

# PROPRIETARY ADMIN SECURITY CONFIG (Hardcoded Bypass with Hashing)
ADMIN_ID = "admin"
ADMIN_HASH = "scrypt:32768:8:1$Cw2lrwbxEaJWsMvM$7d647e7e6e63deab9540306b28ceb1ea622ce0632d2d1b4e10807b507efe42355fab976a9acf2b5c0bc8e4a07ed75c2ba5f8e19330c7e3aac45ee82ceab4ceda"

# Global variables to store loaded models/scalers
rf_model = None
scaler = None
labels = None
label_encoder = None
feature_columns = None
system_status = "ready"  # Track if training is in progress
PULSE_DETECTED = False # Pulse Detection Flag
browser_timer = None   # Global Browser Launch Timer

# --- Global Security Middlewares ---
@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=lambda: session.get('csrf_token'))

@app.before_request
def security_pre_check():
    """Generates CSRF tokens and enforces security validation on sensitive routes."""
    # 1. Ensure CSRF token exists for the session
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)

    # 2. CSRF Validation for all state-changing requests (POST/PUT/DELETE)
    if request.method in ['POST', 'PUT', 'DELETE']:
        # Exempt specific public routes if necessary (None currently)
        exempt_routes = ['/UserLoginAction', '/SignupAction'] # Optional: allow initial auth without token if needed
        if request.path in exempt_routes:
             return
             
        # Check header or form data for the token
        token = request.headers.get('X-CSRF-Token') or request.form.get('csrf_token')
        if not token or token != session.get('csrf_token'):
            return jsonify({"status": "error", "message": "Security Violation: CSRF Token Invalid or Missing"}), 403

@app.after_request
def apply_optimization_headers(response):
    """Hardens the response headers and enables ETag-based caching for optimal reload performance."""
    # 1. Standard security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"

    # 2. Performance: Enable ETag generation for all successful GET requests
    # This allows the browser to perform 'Conditional GETs' (304 Not Modified)
    if request.method == 'GET' and response.status_code == 200:
        response.add_etag()
        response.make_conditional(request)

    # 3. Cache-Control Strategy:
    # - Sensitive user data routes: Strict no-store
    # - Public Templates: allow browser to check for changes (must-revalidate)
    if 'user' in session:
        # For logged-in users, we still need to prevent stale data leaks
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    else:
        # Public landing/login/signup pages: allow caching with revalidation (fastest feel)
        response.headers["Cache-Control"] = "public, no-cache, must-revalidate"
    
    return response

def load_ml_model():
    """Loads the pre-trained model and preprocessing tools from disk."""
    global rf_model, scaler, labels, label_encoder, feature_columns
    try:
        # Base directory of the script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "model", "trained_rf_model.pkl")
        
        if os.path.exists(model_path):
            model_data = joblib.load(model_path)
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
    """API endpoint to clear all app results and terminate session for system reset."""
    if not session.get('user'):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
        
    # Clear all state results (but NOT filesystem credentials as requested)
    session.pop('last_result', None)
    session.pop('train_result', None)
    session.pop('last_page_type', None)
    
    # Also log the user out as requested for a total state reset
    session.pop('user', None)
    session.pop('is_ultimate', None)
    
    return jsonify({"status": "success", "message": "System data cleared and session terminated."})

@app.route('/ClearResults', methods=['POST'])
def ClearResults():
    """Wipes the last analysis results and resets the dashboard state for a fresh start."""
    if 'user' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
        
    session.pop('last_result', None)
    session.pop('last_page_type', None)
    
    return jsonify({"status": "success", "message": "Analysis results wiped successfully."})

@app.route('/api/heartbeat', methods=['GET', 'POST'])
def heartbeat():
    """Silent Heartbeat for Smart Launch and System Status Sync."""
    global browser_timer, PULSE_DETECTED
    
    # Pulse detected! Mark system as having an active session
    PULSE_DETECTED = True
    
    # If a heartbeat arrives, an active tab exists - cancel the startup browser launch
    if browser_timer and browser_timer.is_alive():
        print("[Pulse Detection] Pulse detected from existing tab. Cancelling auto-launch.")
        browser_timer.cancel()
        
    return jsonify({"status": system_status, "health": "online", "pulse": "active"})

# --- Security & User Management ---
USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")

def load_users():
    """Enterprise-grade user directory loader with auto-initialization for master admin."""
    if not os.path.exists(USERS_FILE):
        users = {
            ADMIN_ID: {
                "username": ADMIN_ID,
                "password": ADMIN_HASH,
                "role": "admin"
            }
        }
        save_users(users)
        return users
    
    try:
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
            # Self-healing: Restore master admin if missing from archives
            if ADMIN_ID not in users:
                users[ADMIN_ID] = {
                    "username": ADMIN_ID,
                    "password": ADMIN_HASH,
                    "role": "admin"
                }
                save_users(users)
            return users
    except Exception as e:
        print(f"[Identity Cache] Error: {e}")
        return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/UserLogin', methods=['GET', 'POST'])
def UserLogin():
    if 'user' in session:
        return redirect(url_for('train_view'))
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
            
            # SECURE ADMIN BYPASS (Using Hashed Comparison)
            if creds.get('user') == ADMIN_ID and check_password_hash(ADMIN_HASH, creds.get('pass')):
                session['user'] = ADMIN_ID
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

@app.route('/CheckUsername', methods=['POST'])
def CheckUsername():
    """Real-time identity verification for signup process."""
    data = request.get_json()
    username = data.get('username', '').strip()
    
    if not username:
        return jsonify({"status": "available", "valid": False})
        
    users = load_users()
    if username in users or username.lower() == "admin":
        return jsonify({"status": "taken", "message": "Identity ID already registered in Archives!"})
    
    return jsonify({"status": "available", "message": "Identity available for registration."})

@app.route('/UserLoginAction', methods=['POST'])
def UserLoginAction():
    username = request.form.get('t1')
    password = request.form.get('t2')
    remember = request.form.get('remember') == 'on'
    
    # SECURE ADMIN BYPASS CHECK (Hashed)
    if username == ADMIN_ID and check_password_hash(ADMIN_HASH, password):
        session['user'] = ADMIN_ID
        session['is_ultimate'] = True
        if remember:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(base_dir, "saved_creds.json"), 'w') as f:
                json.dump({"user": ADMIN_ID, "pass": password}, f)
            session['remembered'] = True
        return jsonify({"status": "success", "message": "Ultimate Admin access granted!", "redirect": url_for('train_view')})

    users = load_users()
    user_data = users.get(username)
    
    if not user_data:
        return jsonify({"status": "error", "error_type": "invalid_username", "message": "Identification failed: Username not found."}), 401

    if check_password_hash(user_data['password'], password):
        session['user'] = user_data['username']
        
        # Save credentials locally if "Remember Me" is checked
        if remember:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(base_dir, "saved_creds.json"), 'w') as f:
                json.dump({"user": username, "pass": password}, f)
            session['remembered'] = True
        
        return jsonify({"status": "success", "message": f"Welcome, {username}!", "redirect": url_for('train_view')})
    else:
        return jsonify({"status": "error", "error_type": "invalid_password", "message": "Identification failed: Incorrect password key."}), 401

@app.route('/ResetPasswordAction', methods=['POST'])
def ResetPasswordAction():
    data = request.get_json()
    username = data.get('username')
    new_password = data.get('new_password')
    auto_login = data.get('auto_login', False)
    
    users = load_users()
    if username not in users:
        return jsonify({"status": "error", "message": "User not found in Archives"}), 404
        
    users[username]['password'] = generate_password_hash(new_password)
    save_users(users)
    
    if auto_login:
        session['user'] = username
        return jsonify({"status": "success", "message": "Identity restored. Synchronizing session...", "redirect": url_for('train_view')})
    
    return jsonify({"status": "success", "message": "Security keys updated. Proceed to manual login."})

@app.route('/Signup')
def Signup():
    if 'user' in session:
        return redirect(url_for('train_view'))
    return render_template('Signup.html')

@app.route('/SignupAction', methods=['POST'])
def SignupAction():
    username = request.form.get('username')
    password = request.form.get('password')
    
    users = load_users()
    # Check for both existing users and the reserved master admin identity
    if username in users or username.lower() == "admin":
        return jsonify({"status": "error", "message": "Identity ID already registered in Archives!"}), 400
        
    users[username] = {
        "username": username,
        "password": generate_password_hash(password),
        "role": "user"
    }
    save_users(users)
    return jsonify({
        "status": "success", 
        "message": "Account created successfully!",
        "user_data": {"username": username, "password": password}
    })

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

# Global tracking for pulse-aware auto-launch
browser_timer = None

def open_browser():
    """Enterprise-grade browser launcher with Chrome Incognito forcing."""
    global PULSE_DETECTED
    if PULSE_DETECTED:
        print("[Smart Launch] Aborting: Active pulse detected.")
        return
        
    import subprocess
    url = "http://127.0.0.1:2026/"
    print(f"[Smart Launch] Initializing Incognito Presentation on {url}")
    
    try:
        # Force chrome incognito for a clean, examiner-ready session
        subprocess.Popen(['start', 'chrome', '--incognito', url], shell=True)
    except Exception as e:
        print(f"[-] Smart Launch Error: {e}")
        import webbrowser
        webbrowser.open(url)

def get_project_tree():
    """Neural Discovery: Builds a dynamic, categorical map of the project file system."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Root
    tree = {
        "Technical Docs": [],
        "Model Systems": [],
        "ML Notebooks": [],
        "Environment": []
    }
    
    # Exclude list for the explorer (as requested)
    forbidden_dirs = {'.venv', '.git', '.vscode', '__pycache__', 'Software', 'Project materials', '.ipynb_checkpoints'}
    forbidden_files = {'users.json', '.env', '.gitignore'}

    # Strategy: Scan root and CyberAttackPrediction
    scan_targets = [base_dir, os.path.join(base_dir, 'CyberAttackPrediction'), os.path.join(base_dir, 'docs')]
    
    seen_paths = set()

    for target in scan_targets:
        if not os.path.exists(target): continue
        for item in sorted(os.listdir(target)):
            if item in forbidden_dirs or item in forbidden_files or item.startswith('.'):
                continue
            
            full_item_path = os.path.join(target, item)
            if os.path.isdir(full_item_path): continue # sidebar handles file navigation; directory browsing is inline
            
            # Relative path from Root for URIs
            rel_path = os.path.relpath(full_item_path, base_dir).replace('\\', '/')
            if rel_path in seen_paths: continue
            seen_paths.add(rel_path)

            ext = os.path.splitext(item)[1].lower()
            
            # Categorization Logic
            if ext == '.md' or (ext == '.txt' and 'guide' in item.lower()):
                tree["Technical Docs"].append({"name": item, "path": rel_path})
            elif ext == '.py':
                tree["Model Systems"].append({"name": item, "path": rel_path})
            elif ext == '.ipynb':
                tree["ML Notebooks"].append({"name": item, "path": rel_path})
            elif ext in ['.txt', '.json', '.bat', '.ps1']:
                tree["Environment"].append({"name": item, "path": rel_path})

    return tree

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
    
    # Neural Discovery Tree
    project_tree = get_project_tree()

    # Simple security check to prevent directory traversal
    if '..' in doc_path or doc_path.startswith('/'):
        return render_template('documentation.html', error="Invalid path", project_tree=project_tree)
        
    full_path = os.path.join(base_dir, doc_path)
    if not os.path.exists(full_path):
        return render_template('documentation.html', error=f"Resource not found: {doc_path}", project_tree=project_tree)
        
    try:
        # FOLDER LISTING INTELLIGENCE
        if os.path.isdir(full_path):
            items = []
            for item in sorted(os.listdir(full_path)):
                if not item.startswith('.') and item not in {'.venv', 'Software', 'Project materials'}:
                    item_rel = os.path.join(doc_path, item).replace('\\', '/')
                    is_dir = os.path.isdir(os.path.join(full_path, item))
                    items.append({'name': item, 'path': item_rel, 'is_dir': is_dir})
            
            render_data = {
                'items': items,
                'current_doc': doc_path.replace('\\', '/'),
                'doc_type': 'folder',
                'project_tree': project_tree
            }
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # SPREAD PURE SYNC: Render only the internal macro from documentation.html
                html = render_template_string(
                    "{% from 'documentation.html' import render_doc_fragment %}{{ render_doc_fragment(doc_type, current_doc, items=items) }}",
                    **render_data
                )
                return jsonify({
                    'html': html,
                    'doc_type': 'folder',
                    'path': render_data['current_doc'],
                    'title': doc_path.split('/')[-1] or 'Repository',
                    'breadcrumb': render_data['current_doc'].replace('CyberAttackPrediction/', '')
                })

            return render_template('documentation.html', **render_data)

        ext = os.path.splitext(doc_path)[1].lower()
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        display_path = doc_path.replace('\\', '/')
        if ext == '.md':
            html_content = markdown2.markdown(content, extras=["tables", "fenced-code-blocks", "toc", "header-ids"])
            # Fix image src paths: markdown/HTML files use project-relative paths
            # e.g. "CyberAttackPrediction/static/images/x.png" or "static/images/x.png"
            # Flask serves static at root (static_url_path=''), so correct URL is "/images/x"
            import re as _re
            html_content = _re.sub(
                r'(src=["\'])(?:(?:\.\./)*)(?:CyberAttackPrediction/)?static/images/',
                r'\1/images/',
                html_content
            )
            doc_type = 'markdown'
        elif ext == '.ipynb':
            nb = nbformat.reads(content, as_version=4)
            html_exporter = HTMLExporter()
            html_exporter.template_name = 'basic' # Simple clean output
            (html_content, resources) = html_exporter.from_notebook_node(nb)
            doc_type = 'notebook'
        elif ext in ['.py', '.bat', '.ps1', '.json', '.html', '.css', '.js', '.txt']:
            lexer = get_lexer_for_filename(full_path) if ext != '.txt' else TextLexer()
            formatter = HtmlFormatter(style='monokai', full=False, cssclass="highlight")
            html_content = highlight(content, lexer, formatter)
            doc_type = 'code'
            html_content = f'<style>{formatter.get_style_defs(".highlight")}</style>{html_content}'
        else:
            html_content = f'<pre style="white-space: pre-wrap; word-wrap: break-word;">{content}</pre>'
            doc_type = 'text'

        render_data = {
            'md_content': html_content,
            'current_doc': display_path,
            'doc_type': doc_type,
            'project_tree': project_tree
        }

        # AJAX NEURAL SYNC: Return macro-rendered fragment if requested via AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # SPREAD PURE SYNC: Render only the internal macro from documentation.html
            html = render_template_string(
                "{% from 'documentation.html' import render_doc_fragment %}{{ render_doc_fragment(doc_type, current_doc, md_content=md_content) }}",
                **render_data
            )
            return jsonify({
                'html': html,
                'doc_type': doc_type,
                'path': display_path,
                'title': display_path.split('/')[-1],
                'breadcrumb': display_path.replace('CyberAttackPrediction/', ''),
                'project_tree': project_tree
            })

        return render_template('documentation.html', **render_data)
        
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
    global system_status
    system_status = "busy"
    try:
        result = run_training(dataset_path=custom_path)
        
        # If training was successful, reload the model in memory and persist in session
        if result.get('status') == 'success':
            load_ml_model()
            session['train_result'] = result
            
        return jsonify(result)
    finally:
        system_status = "ready"

@app.errorhandler(404)
def handle_404(e):
    """Premium 404 error handler for CyberShield."""
    return render_template('404.html'), 404

# --- Legal & Contact Routes ---
@app.route('/Contact')
def contact():
    return render_template('Legal.html', section='contact')

@app.route('/TermsOfService')
def terms():
    return render_template('Legal.html', section='terms')

@app.route('/PrivacyPolicy')
def privacy():
    return render_template('Legal.html', section='privacy')

if __name__ == '__main__':
    import sys
    
    # Heartbeat-Aware Smart Launch:
    if '--no-browser' not in sys.argv:
        if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
            print("[Smart Launch] Starting pulse detector (6.5s)...")
            browser_timer = Timer(6.5, open_browser)
            browser_timer.start()
    
    app.run(debug=True, port=2026)

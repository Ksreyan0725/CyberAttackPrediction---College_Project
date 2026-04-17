"""  
================================================================================
PROJECT: CyberShield AI - Bulletproof Command Center (2026)
VERSION: 2.7.1 (Production Hardened - Multi-Alias Engine)
AUTHOR: Ksreyan0725 / Managed by Antigravity AI
PURPOSE: A resilient, zero-failure launcher for the Cyber Attack Prediction project.
FEATURES: Dual-Speed Refresh, Admin Integrity Check, and NLU Command Routing.
LICENSE: College Project - Academic / Open Source
================================================================================
"""
# --- BLOCK 0: LIBRARIES (THE TOOLS) ---
import subprocess  # This library allows Python to run other programs or terminal commands (like 'git' or '.bat' files).
import os          # This library lets Python interact with your files, folders, and operating system (Windows).
import sys         # This library gives Python access to variables used by the computer or the Python interpreter itself.
import time        # This library provides timing functions, like 'time.sleep' for pausing the script.
import json        # NEW: Allows us to save your browser preferences in a file.
import webbrowser  # This library allows Python to automatically open your web browser to a specific web address (URL).
import socket      # NEW: This library allows us to check for an internet connection by 'pinging' a server.
import importlib.util  # NEW: used to check if a specific library is already installed without crashing.
import gc          # NEW: Garbage Collector to ensure memory is cleaned up during long sessions.
import logging     # NEW: Professional logging to track errors in a file.
import msvcrt      # WINDOWS ONLY: Non-blocking input detection.
import ctypes      # WINDOWS ONLY: Attribute management (Hidden files, Admin checks).
import threading   # NEW: Path for non-blocking background tasks (Internet check).
from datetime import datetime # Adds timestamps to logs.

# --- BLOCK 0.5: PREMIUM UI DETECTION ---
try:
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.align import Align
    from rich.live import Live
    from rich.layout import Layout
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False   

# --- BLOCK 0.6: TELEMETRY DETECTION ---
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# --- BLOCK 0.7: UNIFIED CONFIGURATION (CORE SETTINGS) ---
def get_version():
    """Extracts version from the script header docstring dynamically."""
    try:
        with open(__file__, "r", encoding="utf-8") as f:
            for line in f:
                if "VERSION:" in line:
                    # Extracts '2.7.0' from 'VERSION: 2.7.0 (Production Hardened...)'
                    parts = line.split("VERSION:")[1].split("(")
                    return "v" + parts[0].strip()
    except Exception:
        pass
    return "v2.7.0" # Fallback

CONFIG = {
    "PROJECT_NAME": "CyberAttackPrediction",
    "REPO_URL": "https://github.com/Ksreyan0725/CyberAttackPrediction---College_Project",
    "VERSION": get_version(),
    "REFRESH_RATE_FAST": 2.0,  # Stats/Clock
    "REFRESH_RATE_SLOW": 10.0, # Disk/Health scans
    "COMMAND_NAME": "cs",
    "VENV_DIR": ".venv"
}

IS_VIRTUAL = sys.prefix != sys.base_prefix or 'VIRTUAL_ENV' in os.environ
IS_ADMIN = False # Calculated and cached at startup

# --- BLOCK 1.2: PATH CACHE (PRE-COMPUTED TO SAVE CPU) ---
root_dir = os.path.dirname(os.path.abspath(__file__))

PATHS = {
    "root": root_dir,
    "project": os.path.join(root_dir, CONFIG["PROJECT_NAME"]),
    "model": os.path.join(root_dir, CONFIG["PROJECT_NAME"], "model"),
    "venv": os.path.join(root_dir, CONFIG["VENV_DIR"]),
    "requirements": os.path.join(root_dir, CONFIG["PROJECT_NAME"], "requirements.txt"),
    "log": os.path.join(root_dir, "launcher_debug.log"),
    "settings": os.path.join(root_dir, "launcher_settings.json"),
    "venv_exe": os.path.join(root_dir, CONFIG["VENV_DIR"], "Scripts", "python.exe")
}

VENV_PATH = sys.prefix if IS_VIRTUAL else sys.base_prefix
VENV_NAME = os.path.basename(VENV_PATH) if IS_VIRTUAL else "Global Python"
REPO_URL  = CONFIG["REPO_URL"]

# --- BLOCK 1.5: VISUAL ENGINE (THE COLORS) ---
# These are ANSI escape codes. They tell the terminal to change the text color.
# Standard: \033[91m = Red, \033[92m = Green, etc. \033[0m = Reset to default.
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
RESET   = "\033[0m"
BOLD    = "\033[1m"
LOG_FILE = PATHS["log"]
SETTINGS_FILE = PATHS["settings"]

def is_admin():
    """PURPOSE: Checks if the launcher is running with Administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def hide_file(path):
    """PURPOSE: Makes a file hidden on Windows (like .git)."""
    if os.name == 'nt' and os.path.exists(path):
        try:
            # 2 is the constant for Hidden attribute in Windows
            ctypes.windll.kernel32.SetFileAttributesW(path, 2)
        except Exception:
            pass

def log_system_event(message, level="INFO"):
    """
    PURPOSE: This is like an 'Airplane Black Box'. 
    If something crashes, this function writes exactly what happened to 'launcher_debug.log'.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
        # Note: log file hiding is now handled once at session start for performance.
    except Exception:
        pass # We don't want the logger to crash the launcher!

# Initialize log file with a 'Start' session marker
log_system_event("--- New Command Center Session Started ---")

def load_settings():
    """PURPOSE: Loads your saved preferences (like Browser Mode) from the JSON file."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_settings(settings):
    """PURPOSE: Saves your preferences so the script remembers them next time."""
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
        hide_file(SETTINGS_FILE) # Ensure the settings stay hidden
    except Exception as e:
        log_system_event(f"Failed to save settings: {e}", level="ERROR")

# --- BLOCK 3: UTILITY HELPERS (THE BACKGROUND ENGINE) ---
def clear_keyboard_buffer():
    while msvcrt.kbhit():
        try:
            msvcrt.getch()
        except:
            pass
    time.sleep(0.05) 
# --- BLOCK 2: ASYNC CONNECTIVITY SHIELD ---
_INTERNET_STATUS = True # Shared variable for background thread

def connectivity_guard():
    """PURPOSE: A background thread that checks internet health without lag."""
    global _INTERNET_STATUS
    while True:
        try:
            # Pinging Google DNS (Fastest check)
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            _INTERNET_STATUS = True
        except (OSError, socket.timeout):
            _INTERNET_STATUS = False
        time.sleep(30) # Only check every 30s to save CPU/Battery

def check_internet():
    """PURPOSE: Returns the cached internet status from the background guard."""
    return _INTERNET_STATUS

def get_requirements():
    """
    PURPOSE: Reads the project's 'shopping list' of libraries from requirements.txt.
    """
    req_path = PATHS["requirements"]
    if not os.path.exists(req_path):
        log_system_event("requirements.txt missing", level="WARNING")
        return [] # Return empty list if the file is missing.
    
    requirements = []
    try:
        # encoding="utf-8": Ensures the script works on computers in any country (like India) without crashing on weird symbols.
        with open(req_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip comments (#) and empty lines to avoid errors.
                if line and not line.startswith("#"):
                    requirements.append(line)
    except Exception:
        pass
    return requirements

def is_package_installed(package_name):
    """
    PURPOSE: Checks if a specific library (like 'pandas') is already functioning in your Python.
    """
    # We clean the package name (e.g. 'pandas==3.0.2' -> 'pandas')
    clean_name = package_name.split('==')[0].split('>=')[0].strip()
    return importlib.util.find_spec(clean_name) is not None

# --- BLOCK 3: THE LAUNCHER FUNCTIONS (THE ACTIONS) ---

def run_script(script_name, new_window=False):
    """
    PURPOSE: This function is the engine that launches your project dashboards.
    - script_name: The name of the file to run (like 'Start_WebApp_Venv.bat').
    - new_window: A 'True/False' check. If True, it spawns a fresh separate terminal window.
    """
    # os.path.join: This smartly combines 'Project Folder' + 'Script Name' into a valid Windows path.
    script_path = os.path.join(root_dir, script_name)

    # os.path.exists: This checks if the file is actually there. If not, we print an error instead of crashing.
    if not os.path.exists(script_path):
        print(f"[-] Error: Script '{script_name}' not found.")
        return # 'return' exits the function immediately if the file is missing.

    # This creates a label to tell the user HOW the script is starting.
    mode_label = "NEW TERMINAL" if new_window else "INTEGRATED"
    print(f"[+] Launching CyberShield Engine ({mode_label})")
    print(f"[+] Script: {script_name}")
    print("--------------------------------------------------")
    
    try:
        if new_window:
            # subprocess.Popen: This starts a process in the background.
            # 'start cmd /k': This is a Windows-specific command to open a new Command Prompt window and Keep (/k) it open.
            subprocess.Popen(['start', 'cmd', '/k', script_path], shell=True)
            print(f"{GREEN}[*] Process spawned in separate window successfully.{RESET}")
        else:
            # subprocess.run: This runs the command right here and WAITS for it to finish.
            # check=True: This means if the script fails, Python will raise an error so we can catch it.
            subprocess.run([script_path], shell=True, check=True)
            
    except KeyboardInterrupt:
        # This catches when you press Ctrl+C to stop a program manually.
        print(f"\n{YELLOW}[!] Launcher: Process interrupted by user.{RESET}")
    except Exception as e:
        # This catches any other random error (like a missing file or permission issue) and shows you exactly what went wrong ({e}).
        log_system_event(f"Script Execution Error ({script_name}): {str(e)}", level="ERROR")
        print(f"\n{RED}[-] Launcher Error: {e}{RESET}")

def harden_environment():
    """
    PURPOSE: This is the 'Real System Doctor'. 
    It checks your internet, upgrades Pip, and installs every required library with retry logic.
    """
    # Pillar 6: Connectivity Check
    if not check_internet():
        print(f"\n{RED}[!] CRITICAL: No internet connection detected.{RESET}")
        print("[!] The Hardening Engine requires a connection for the first-time setup.")
        input(f"\n{YELLOW}[PAUSED] Please connect to the internet and press ENTER to try anyway...{RESET}")

    # Step 0: Pip Integrity Check
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except Exception:
        log_system_event("Pip is not functional or missing from the current Python path.", level="CRITICAL")
        print("\n[!] CRITICAL ERROR: Python Package Manager (Pip) is broken.")
        print("[!] Please reinstall Python or fix your installation paths.")
        input("\nPress ENTER to return to menu...")
        return

    try:
        # Step 1: Ensure 'rich' is available for the premium UI.
        if not is_package_installed("rich"):
            print("[*] Installing TUI Engine (Rich)...")
            res = subprocess.run([sys.executable, "-m", "pip", "install", "rich"], capture_output=True, text=True)
            if res.returncode != 0:
                log_system_event(f"Failed to install 'rich'. Error: {res.stderr}", level="ERROR")
        
        # Lazy Loading imports to prevent crashes.
        from rich.console import Console
        from rich.panel import Panel
        from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID
        from rich.table import Table
        from rich.text import Text
        
        console = Console()
        
        # Header Display
        header_text = Text("🛡️ CyberShield AI: THE BULLETPROOF HARDENING ENGINE (2026)", style="bold cyan")
        console.print(Panel(header_text, border_style="bright_blue", expand=False))
        
        # Diagnostic Table
        table = Table(title="[SYSTEM DIAGNOSTIC]", show_header=True, header_style="bold magenta")
        table.add_column("Component", style="cyan")
        table.add_column("Status / Version", style="green")
        table.add_row("Python Core", f"{sys.version.split()[0]} (Verified)")
        table.add_row("Environment", f"VIRTUAL ({VENV_NAME})" if IS_VIRTUAL else "GLOBAL (Manual)")
        table.add_row("Network", "ONLINE (Stable)" if check_internet() else "OFFLINE (Limited)")
        console.print(table)
        
        # --- THE REAL INSTALLATION ENGINE ---
        requirements = get_requirements()
        if not requirements:
            console.print("[yellow][!] Warning: No requirements.txt found. Skipping library sync.[/yellow]")
            # The 'Bulletproof' line-up of libraries needed for your project.
            required_packages = ["rich", "requests", "psutil", "numpy", "pandas", "scikit-learn"] # Fallback essentials
            requirements = required_packages
        
        # Step 2: Force-Upgrade Pip (The foundational tool)
        console.print("\n[*] Hardening Package Manager (Pip)...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], capture_output=True)

        # Step 3: Install libraries with progress tracking
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(pulse_style="bright_cyan"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            expand=True
        ) as progress:
            
            total_task = progress.add_task("[cyan]Overall Progress", total=len(requirements))
            
            for pkg in requirements:
                pkg_clear = pkg.split('==')[0] # Clean name for display
                progress.update(total_task, description=f"[magenta]Hardening: {pkg_clear}")
                
                success = False
                for attempt in range(4): # 4 attempts: 1 normal + 3 retries
                    try:
                        # TRIPLE LOCK CHECK: Internet Recovery
                        if not check_internet():
                            progress.print(f"[yellow][!] Connection Lost. Waiting for recovery...[/yellow]")
                            while not check_internet():
                                time.sleep(5)
                            progress.print(f"[green][+] Connection Restored. Resuming {pkg_clear}...[/green]")

                        # Run the install silently
                        subprocess.run(
                            [sys.executable, "-m", "pip", "install", pkg, "--retries", "10", "--timeout", "60"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
                        )
                        success = True
                        break
                    except subprocess.CalledProcessError as e:
                        # Capture detailed error on failure for logging
                        log_res = subprocess.run(
                            [sys.executable, "-m", "pip", "install", pkg],
                            capture_output=True, text=True
                        )
                        err_msg = log_res.stderr.lower()
                        
                        log_system_event(f"Hardening Failure (Pkg: {pkg}): {log_res.stderr}", level="ERROR")
                        
                        if "permission denied" in err_msg or "access is denied" in err_msg:
                            progress.print(f"[red][!] ACCESS DENIED: Please run this launcher as ADMINISTRATOR.[/red]")
                            break # No point retrying if permissions are blocked
                        elif "no space left" in err_msg:
                            progress.print(f"[red][!] DISK FULL: Free up space on your drive.[/red]")
                            break
                        
                        progress.print(f"[yellow][!] Retry {attempt+1}/3 for {pkg_clear}...[/yellow]")
                        time.sleep(2)
                    except Exception as ex:
                        log_system_event(f"Unexpected installation error: {str(ex)}", level="ERROR")
                        time.sleep(2)
                
                if not success:
                    progress.print(f"[red][-] Failure: {pkg_clear} could not be hardened. Check launcher_debug.log[/red]")
                
                progress.advance(total_task)

        console.print("\n✅ [bold green]ZERO-FAILURE HARDENING COMPLETE[/bold green] 🛡️")
        console.print("--------------------------------------------------")
        
    except Exception as e:
        # This is the 'Doctor's Emergency' block. If the main hardening engine fails (like a weird permission crash),
        # we don't just stop; we try to run the backup PowerShell script (install_deps.ps1).
        print(f"[-] Critical Engine Error: {e}")
        print("[!] Falling back to emergency PowerShell script...")
        # 'powershell -ExecutionPolicy Bypass': This tells Windows to allow running our setup script.
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "install_deps.ps1"])
    
    input("\n[PROCESSS COMPLETE] Press ENTER to return to menu...")

def show_help(query=None):
    """
    PURPOSE: This is the 'Quick Guide'. It prints specifically what you need to know.
    If a query is provided (e.g., 'git'), it highlights relevant commands.
    """
    print("\n" + "="*42)
    print("   🛡️ CyberShield AI - COMMAND HELP        ")
    print("="*42)
    
    help_data = [
        ("1/run/start/dashboard", "Launch Dashboard (Integrated)"),
        ("2/ext", "Launch Dashboard (External Window)"),
        ("3/jupyter/notebook", "Launch Jupyter (Integrated)"),
        ("4", "Launch Jupyter (External Window)"),
        ("5/harden/setup/fix", "Harden Environment (Self-Repair)"),
        ("6/github/repo/source", "Open GitHub Repository"),
        ("7/venv/switch", "Switch to Virtual Environment"),
        ("8/upgrade/migrate", "Auto-upgrade to Venv & Restart"),
        ("9/pull/update", "Git: Pull latest code changes"),
        ("10/push/sync", "Git: Commit and Push changes"),
        ("11/ignore", "Git: Edit .gitignore file"),
        ("12/audit/version/path", "Check Python Versions & Paths"),
        ("13/restart/refresh", "Restart the Launcher"),
        ("14/exit/stop/quit", "Close the Launcher"),
        ("15/global/cs/register", "Enable Global 'cs' Command"),
        ("16/reset", "Reset Browser Preferences"),
        ("17/bro/cyber/alias", "Enable ALL Global Aliases (cs, bro, cyber)"),
        ("18/speed/network/test", "Run Network Speed Test"),
        ("19/help/guide", "Open Comprehensive Help Guide"),
        ("20/log/logs/audit", "View Audit Logs (Notepad)")
    ]
    
    found = False
    query_str = str(query).lower() if query else ""
    
    for cmd, desc in help_data:
        # If no query, or if query matches either the command list or description
        if not query or query_str in cmd.lower() or query_str in desc.lower():
            label = f"{CYAN}{cmd:25}{RESET}"
            print(f" {label} : {desc}")
            found = True
            
    if not found:
        print(f"{YELLOW}[!] No specific help for '{query}'. Showing all commands:{RESET}")
        for cmd, desc in help_data:
            print(f" {CYAN}{cmd:25}{RESET} : {desc}")

    print("\n[TIP] You can speak naturally: 'help git', 'run help', or 'harden fix'.")
    print("="*42)
    input("Press ENTER to return to menu...")

def check_system_paths():
    """
    PURPOSE: This is the 'Path Finder'. It checks exactly WHERE your Python is installed.
    Highly useful for debugging 'Python not found' errors.
    """
    print("\n==========================================")
    print("   CyberShield AI - SYSTEM DIAGNOSTIC   ")
    print("==========================================")
    try:
        # 'where python' is a Windows command that searches all your system paths for python.exe.
        print("[*] Python Executable Locations (where python):")
        subprocess.run(["where", "python"], check=False)
        
        # 'python --version' asks the program to identify its exact version number.
        print("\n[*] Python Core Version (python --version):")
        subprocess.run(["python", "--version"], check=False)
        
        # 'pip --version' checks your library manager.
        print("\n[*] Package Manager Version (pip --version):")
        subprocess.run(["pip", "--version"], check=False)
        
        # 'sys.executable': This is the EXACT folder path of the Python brain currently running THIS script.
        # 'sys.prefix': The main folder containing your Python installation.
        print("\n[*] Current Runtime Environment:")
        print(f"    Active Python: {sys.executable}")
        print(f"    Active Prefix: {sys.prefix}")
        print(f"    Is Virtual:    {IS_VIRTUAL}")
    except Exception as e:
        print(f"[-] Diagnostic Error: {e}")
    
    print("==========================================")
    input("[AUDIT COMPLETE] Press ENTER to return to menu...")

def get_system_stats():
    """
    PURPOSE: This reads your computer's pulse (CPU/RAM).
    """
    if not HAS_PSUTIL:
        return {"cpu": 0, "ram": 0, "disk": 0}
    
    try:
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        return {"cpu": cpu, "ram": ram, "disk": disk}
    except Exception:
        return {"cpu": 0, "ram": 0, "disk": 0}

def get_project_health():
    """
    PURPOSE: The Unified Health Engine (Optimized).
    Scans for ML models and calculates a 0-100% score using single-pass I/O.
    """
    # 1. SCAN FOR CORE MODELS (SINGLE-PASS DIR SCAN)
    core_weights = {
        "dos_weight.hdf5", "ids_weight.hdf5", "iot_weight.hdf5", 
        "kdd_weight.hdf5", "trained_rf_model.pkl"
    }
    
    found_count = 0
    missing = list(core_weights)
    
    if os.path.exists(PATHS["model"]):
        try:
            # os.listdir is much faster than 5 separate os.path.exists calls
            present_files = set(os.listdir(PATHS["model"]))
            for w in core_weights:
                if w in present_files:
                    found_count += 1
                    missing.remove(w)
        except Exception:
            pass # Use fallback behavior if dir read fails
            
    # 2. EVALUATE STATUS
    status, msg, color = "HEALTHY", "All systems nominal.", "green"
    if len(missing) > 0:
        if len(missing) < 3:
            status, msg, color = "WARNING", f"Missing {len(missing)} model(s): {', '.join(missing)}", "yellow"
        else:
            status, msg, color = "CRITICAL", "Major components missing! Run option 5.", "red"
            
    # 3. CALCULATE NUMERIC SCORE (0-100)
    score = 0
    if IS_VIRTUAL: score += 20
    if HAS_RICH: score += 15
    if HAS_PSUTIL: score += 15
    if found_count >= 3: score += 40
    elif found_count > 0: score += 20
    if check_internet(): score += 10
    
    # 4. FINAL ADAPTIVE SCORING (User vs Admin)
    # In User mode, we cap the 'Operational' score at 100% if everything else is perfect.
    # We still track Admin Integrity separately for the 'Ready' badge.
    if IS_ADMIN:
        score_label = f"READY: {score}% [dim](System Integrity Locked)[/]" if score < 100 else "READY: 100% [bold green](SHIELD ACTIVE)[/]"
    else:
        # Penalize slightly for lack of admin if it affects core functionality (it doesn't usually, but it's good to note)
        score_label = f"READY: {score}% [dim](User Mode)[/]"
    
    return {
        "status": status,
        "msg": msg,
        "color": color,
        "score": score,
        "label": score_label
    }

def find_browser_exe():
    """
    PURPOSE: Scans the computer for Chrome, Edge, or Firefox.
    Priority: Chrome (Incognito) > Edge (InPrivate) > Firefox (Private Window).
    """
    paths = {
        "chrome": [
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Google\\Chrome\\Application\\chrome.exe"),
            os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Google\\Chrome\\Application\\chrome.exe"),
            os.path.join(os.environ.get("LocalAppData", ""), "Google\\Chrome\\Application\\chrome.exe")
        ],
        "edge": [
            os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Microsoft\\Edge\\Application\\msedge.exe"),
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Microsoft\\Edge\\Application\\msedge.exe")
        ],
        "firefox": [
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Mozilla Firefox\\firefox.exe"),
            os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Mozilla Firefox\\firefox.exe")
        ]
    }
    
    # Check Chrome
    for p in paths["chrome"]:
        if os.path.exists(p): return p, "chrome", "--incognito"
    # Check Edge
    for p in paths["edge"]:
        if os.path.exists(p): return p, "edge", "--inprivate"
    # Check Firefox
    for p in paths["firefox"]:
        if os.path.exists(p): return p, "firefox", "-private-window"
        
    return None, None, None

def open_repo_smart():
    """
    PURPOSE: Handles the opening of the GitHub Repo with Smart Preferences.
    """
    settings = load_settings()
    mode = settings.get("browser_mode")
    
    if not mode:
        print(f"\n{CYAN}[?] BROWSER PREFERENCE REQUIRED]{RESET}")
        print("1. Default System Browser (Standard)")
        print("2. Incognito/Private Mode (Chrome/Edge/Firefox)")
        choice = input(f"\n{YELLOW}Select Mode (The script will REMEMBER this): {RESET}").strip()
        
        if choice == '2':
            mode = "incognito"
        else:
            mode = "standard"
        
        settings["browser_mode"] = mode
        save_settings(settings)
        print(f"{GREEN}[+] Preference saved! (Use Maintenance menu to reset later).{RESET}")

    if mode == "incognito":
        exe_path, name, flag = find_browser_exe()
        if exe_path:
            print(f"[*] Launching {name.title()} in Private Mode...")
            try:
                subprocess.Popen([exe_path, flag, REPO_URL])
                return
            except Exception as e:
                log_system_event(f"Incognito launch failed: {e}", level="ERROR")
        
        print(f"{YELLOW}[!] No private-capable browser found. Falling back to default.{RESET}")

    # Standard Fallback
    print(f"[*] Launching Repository: {REPO_URL}")
    webbrowser.open(REPO_URL)

def setup_global_access(command_name="cs"):
    """
    PURPOSE: This registers the 'cs' command globally on the computer.
    It creates a .bat file and adds the folder to the Windows PATH.
    """
    if HAS_RICH:
        console.print(f"\n[*] Initializing Global Registration for command: '{command_name}'...")
    else:
        print(f"\n[*] Initializing Global Registration for command: '{command_name}'...")
        
    try:
        # Step 1: Create the .bat shim
        shim_path = os.path.join(root_dir, f"{command_name}.bat")
        python_exe = sys.executable 
        script_path = os.path.join(root_dir, "launcher.py")
        
        # We use @echo off to keep the terminal clean
        # %* allows the user to pass arguments like 'cs help'
        content = f"@echo off\n\"{python_exe}\" \"{script_path}\" %*\n"
        
        with open(shim_path, "w") as f:
            f.write(content)
            
        # Step 2: Add directory to PATH using PowerShell (Safer than setx for long paths)
        # We add it to the 'User' path, which doesn't require Admin for the owner.
        cmd = f'powershell -Command "[Environment]::SetEnvironmentVariable(\'Path\', [Environment]::GetEnvironmentVariable(\'Path\', \'User\') + \';{root_dir}\', \'User\')"'
        subprocess.run(cmd, shell=True, check=True)
        
        msg = f"SUCCESS: You can now type '{command_name}' in any NEW terminal window!"
        if HAS_RICH:
            console.print(Panel(msg, border_style="green"))
        else:
            print(f"\n[+] {msg}")
            
        log_system_event(f"Registered global command: {command_name}", level="INFO")
    except Exception as e:
        err = f"Registration Failed: {e}"
        if HAS_RICH:
            console.print(Panel(err, border_style="red"))
        else:
            print(f"\n[-] {err}")
        log_system_event(err, level="ERROR")
    
    input("\nPress ENTER to return to menu...")

def setup_all_aliases():
    """PURPOSE: Mass-registers 'cs', 'bro', and 'cyber' as global commands."""
    aliases = ["cs", "bro", "cyber"]
    if HAS_RICH:
        console.print(Panel(f"🚀 REGISTERING MULTI-ALIAS SYSTEM: {', '.join(aliases)}", border_style="cyan"))
    
    success_count = 0
    for alias in aliases:
        try:
            shim_path = os.path.join(PATHS["root"], f"{alias}.bat")
            python_exe = sys.executable 
            script_path = os.path.join(PATHS["root"], "launcher.py")
            content = f"@echo off\n\"{python_exe}\" \"{script_path}\" %*\n"
            
            with open(shim_path, "w") as f:
                f.write(content)
            success_count += 1
        except Exception as e:
            log_system_event(f"Failed to create shim for {alias}: {e}", level="ERROR")

    try:
        # Update PATH once for the whole directory
        cmd = f'powershell -Command "[Environment]::SetEnvironmentVariable(\'Path\', [Environment]::GetEnvironmentVariable(\'Path\', \'User\') + \';{PATHS["root"]}\', \'User\')"'
        subprocess.run(cmd, shell=True, check=True)
        
        msg = f"SUCCESS: Multi-Alias Engine Active! ({success_count}/{len(aliases)} shims created)."
        if HAS_RICH:
            console.print(Panel(msg, border_style="green"))
        else:
            print(f"\n[+] {msg}")
        print(f"[*] You can now use: '{BOLD}cs{RESET}', '{BOLD}bro{RESET}', or '{BOLD}cyber{RESET}' from any terminal.")
    except Exception as e:
        log_system_event(f"Multi-Path update failed: {e}", level="ERROR")
        print(f"{RED}[-] System Path Update Failed: {e}{RESET}")

    input("\nPress ENTER to return to menu...")

def run_speed_test():
    """
    PURPOSE: Measures real-time internet bandwidth in MB/s with a live meter.
    Method: Downloads a 10MB file in chunks and calculates throughput.
    """
    test_url = "https://speed.hetzner.de/10MB.bin"
    
    if not check_internet():
        print(f"\n{RED}[-] SPEED TEST FAILED: No internet connection.{RESET}")
        input("Press ENTER to return to menu...")
        return

    # Dynamic imports for specific rich features
    try:
        import requests
        from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn
    except ImportError:
        print(f"{YELLOW}[!] Missing 'requests' or 'rich'. Run Option 5 (Harden) first.{RESET}")
        input("Press ENTER to return...")
        return

    if HAS_RICH:
        console.print(Panel(Align.center("[bold cyan]🚀 INITIALIZING NETWORK SPEED DIAGNOSTIC...[/bold cyan]"), border_style="cyan"))
    else:
        print("\n[*] Initializing Network Speed Test...")

    try:
        start_time = time.time()
        # Stream=True allows us to process the file in real-time bits
        response = requests.get(test_url, stream=True, timeout=15)
        total_size = int(response.headers.get('content-length', 0))
        
        if total_size == 0:
            raise Exception("Invalid response from server (0 bytes)")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=None, pulse_style="bright_cyan"),
            "[progress.percentage]{task.percentage:>3.0f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            expand=True
        ) as progress:
            
            task = progress.add_task("[magenta]Testing Pulse...", total=total_size)
            
            downloaded = 0
            for chunk in response.iter_content(chunk_size=512*1024): # 512KB chunks
                if chunk:
                    downloaded += len(chunk)
                    progress.update(task, completed=downloaded)
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Final Calculation
            final_mb = downloaded / (1024 * 1024)
            avg_speed = final_mb / duration if duration > 0 else 0
            
            # Result UI
            status_text = "EXCELLENT" if avg_speed > 10 else "STABLE" if avg_speed > 2 else "SLUGGISH"
            color = "green" if avg_speed > 10 else "yellow" if avg_speed > 2 else "red"
            
            msg = f"Network Pulse: {avg_speed:.2f} MB/s ({status_text})"
            if HAS_RICH:
                console.print(Panel(Align.center(f"[bold {color}]{msg}[/]"), border_style=color, title="[Diagnostic Result]"))
            else:
                print(f"\n[+] Speed: {avg_speed:.2f} MB/s - {status_text}")
                
            log_system_event(f"Network Speed Test Complete: {avg_speed:.2f} MB/s", level="INFO")

    except Exception as e:
        log_system_event(f"Speed Test Error: {e}", level="ERROR")
        print(f"\n{RED}[-] Diagnostic Interrupted: {e}{RESET}")
        print("[!] Tip: This may be due to a strict firewall or temporary server outage.")

    input("\nPress ENTER to return to menu...")

def get_input_timeout(prompt, timeout=2.0):
    """
    PURPOSE: This is a Windows-specific trick to wait for a user's input
    without pausing the whole script. If the user doesn't type anything within
    the timeout, the script continues (allowing us to refresh the telemetry).
    """
    if HAS_RICH:
        console.print(prompt, end="")
    else:
        print(prompt, end="", flush=True)
        
    start_time = time.time()
    user_input = ""
    
    while (time.time() - start_time) < timeout:
        if msvcrt.kbhit():
            try:
                raw = msvcrt.getch() # Use getch (no echo) for better control
                # Handle Windows special keys (Arrow keys, F-keys)
                if raw in [b'\xe0', b'\x00']:
                    if msvcrt.kbhit(): msvcrt.getch() # Swallow the second byte
                    continue
                
                char = raw.decode('utf-8', errors='ignore')
                if not char: continue

                if char in ['\r', '\n']: # Enter key
                    print() # Move to next line
                    return user_input.strip()
                elif char == '\x08': # Backspace (standard byte for \b)
                    if len(user_input) > 0:
                        user_input = user_input[:-1]
                        print("\b \b", end="", flush=True)
                elif char.isprintable():
                    user_input += char
                    print(char, end="", flush=True)
            except Exception:
                pass 
        time.sleep(0.01)
    
    return None # Indicates a timeout (refresh the screen)

# --- BLOCK 3: THE MAIN BRAIN (THE INTERFACE) ---

def render_premium_menu(health_data=None, current_input=""):
    """
    PURPOSE: This is the 'Wow Factor' UI. It builds a beautiful two-column dashboard.
    RETURNS: A Rich Renderable (Group) for Live display.
    """
    if not HAS_RICH:
        return "" 

    # 0. FETCH DATA
    stats = get_system_stats()
    
    # Use cached health data or fetch if missing
    h = health_data if health_data else get_project_health()
    
    # 0. HEADER WITH LIVE CLOCK & ADMIN STATUS
    now = datetime.now().strftime("%I:%M:%S %p")
    admin_tag = "[bold green]ADMIN[/]" if IS_ADMIN else "[bold yellow]USER[/]"
    
    # 💡 REFINED HEADING: Unified Info Box as requested
    header_grid = Table.grid(expand=True)
    header_grid.add_column(justify="left")
    header_grid.add_column(justify="center")
    header_grid.add_column(justify="right")
    
    env_badge = f"[bold white]Env:[/] [bold {('green' if IS_VIRTUAL else 'yellow')}]{VENV_NAME}[/]"
    center_title = f"🛡️  [bold cyan]CYBERSHIELD COMMAND CENTER[/]  [dim]{CONFIG['VERSION']}[/]"
    status_badge = f"{admin_tag} | [bold cyan]{now}[/]"
    
    header_grid.add_row(env_badge, center_title, status_badge)
    header_panel = Panel(header_grid, border_style="cyan", padding=(0, 1))

    # 1. TOP BAR: SYSTEM STATUS (Real-time Telemetry)
    # 💡 Optimization: We merge integrity and Python runtime into this bar
    stats_text = Text.assemble(
        (f"💻 CPU: {stats['cpu']}% ", "bold green" if stats['cpu'] < 70 else "bold red"),
        (f" | 💾 RAM: {stats['ram']}% ", "bold blue" if stats['ram'] < 80 else "bold red"),
        (f" | 📂 DISK: {stats['disk']}% ", "bold white"),
        (" | ", "white"),
        Text.from_markup(f"[bold {h['color']}]Integrity: {h['status']}[/]"),
        (" | ", "white"),
        Text.from_markup(f"[bold cyan]Py: {sys.executable.split('\\')[-1]}[/]")
    )
    
    telemetry_panel = Panel(Align.center(stats_text), border_style="bright_blue", padding=(0, 2))
    
    # 💡 The 1.5 Health/Py badges are now integrated into the telemetry bar above.
    health_banner = None

    # 2. THE DASHBOARD GRID
    if IS_ADMIN:
        # POWER-USER GRID (Rainbow Boxes)
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="left", ratio=1)

        launch_panel = Panel(
            "[bold green]1.[/] WebApp (Integrated)\n[bold green]2.[/] WebApp (External)\n[bold green]3.[/] Jupyter Notebook\n[bold green]4.[/] Jupyter (External)",
            title="[bold green]🚀 ENGINE LAUNCH[/]", border_style="green", padding=(0, 2), expand=True
        )
        system_panel = Panel(
            "[bold magenta]5.[/] Harden Environment\n[bold magenta]6.[/] GitHub Repo\n[bold magenta]7.[/] Switch to Venv\n[bold magenta]8.[/] Auto-Upgrade",
            title="[bold magenta]🛠️ SYSTEM OPS[/]", border_style="magenta", padding=(0, 2), expand=True
        )
        git_panel = Panel(
            "[bold yellow]9.[/] Git: Pull Code\n[bold yellow]10.[/] Git: Sync/Push\n[bold yellow]11.[/] Git: Edit Ignore",
            title="[bold yellow]📦 VERSION CONTROL[/]", border_style="yellow", padding=(0, 2), expand=True
        )
        
        # 💡 MAINTENANCE: Multi-column to save vertical space in Admin Mode
        maint_grid = Table.grid(expand=True)
        maint_grid.add_column(ratio=1)
        maint_grid.add_column(ratio=1)
        
        maint_grid.add_row("12. System Audit", "13. Force Restart")
        maint_grid.add_row("[bold red]14. Exit Launcher[/]", "[bold yellow]15. Enable 'cs'[/]")
        maint_grid.add_row("16. Reset Browser", "[bold cyan]17. Reg Aliases[/]")
        maint_grid.add_row("[bold green]18. Speed Test[/]", "19. Help Guide")
        maint_grid.add_row("20. Audit Logs", "")
        
        maint_panel = Panel(maint_grid, title="[bold blue]🛡️ MAINTENANCE[/]", border_style="blue", padding=(0, 2), expand=True)
        
        grid.add_row(launch_panel, system_panel)
        grid.add_row(git_panel, maint_panel)
        main_display = grid
    else:
        # 💡 MINIMALIST RED PANEL (User Mode Only)
        hub_grid = Table.grid(expand=True, padding=(0, 2))
        hub_grid.add_column(ratio=1)
        hub_grid.add_column(ratio=1)
        hub_grid.add_column(ratio=1)
        
        col1 = (
            "[bold green]1.[/] WebApp (Int)\n"
            "[bold green]2.[/] WebApp (Ext)\n"
            "[bold green]3.[/] Jupyter NB\n"
            "[bold green]4.[/] Jupyter (Ext)"
        )
        col2 = (
            "[bold magenta]5.[/] Harden Env\n"
            "[bold magenta]6.[/] GitHub Repo\n"
            "[bold magenta]7.[/] Switch Venv\n"
            "[bold magenta]8.[/] Auto-Upgrade"
        )
        col3 = (
            "[bold yellow]9. [/] Git Pull\n"
            "[bold yellow]10.[/] Git Sync\n"
            "[bold yellow]11.[/] Edit Ignore\n"
            "[bold cyan]12.[/] Diagnostic\n"
            "[bold cyan]13.[/] RESTART\n"
            "[bold red]14. EXIT HUB[/]"
        )
        
        hub_grid.add_row(col1, col2, col3)
        main_display = Panel(hub_grid, title="[bold red]⚡ CYBER SENTINEL HUB[/]", border_style="red", padding=(0, 2))

    # 3. PROMPT DISPLAY (Embedded Input)
    prompt_tag = "cmd_admin" if IS_ADMIN else "cmd_cyber"
    input_line = Text.from_markup(f"[bold cyan]{prompt_tag}[/] > [white]{current_input}[/]", style="white")
    
    # High-Visibility Cursor Block
    if int(time.time() * 2) % 2 == 0: 
        input_line.append("_", style="bold cyan")
    
    prompt_panel = Panel(input_line, border_style="cyan", padding=(0, 2))

    # 4. ASSEMBLE ALL COMPONENTS
    components = [header_panel]
    
    components.append(telemetry_panel)
    components.append(main_display)
    components.append(prompt_panel) # Always show the prompt embedded
    components.append(Text(f"Tip: Type 'help' for details | Session Log: {LOG_FILE}", style="white"))
    
    return Group(*components)

def boot_loader():
    """PURPOSE: A high-tech 'Boot Sequence' for a professional first impression."""
    if not HAS_RICH:
        return

    # 💡 IMPROVEMENT: Turbo Mode (Skip animation if recently booted)
    settings = load_settings()
    turbo_mode = settings.get("turbo_mode", False)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Force enable ANSI escape sequences for Windows
    if os.name == 'nt':
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    from rich.columns import Columns
    from rich.live import Live
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    
    # 1. THE LOGO REVEAL
    logo = f"""[bold red]
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗██╗  ██╗██╗███████╗██╗     ██████╗ 
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗███████║██║█████╗  ██║     ██║  ██║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║██║  ██║██║███████╗███████╗██████╔╝
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝ 
[/]
[dim cyan]      SYSTEM INITIALIZATION | COMMAND CENTER {CONFIG['VERSION']} | 2026 PRODUCTION [/]"""
    console.print(Align.center(logo))
    
    if turbo_mode:
        console.print(Align.center("[dim italic]Turbo Mode Active: Skipping Animation...[/]"))
        time.sleep(0.3)
    else:
        time.sleep(0.5)

        # 2. THE BOOT DIAGNOSTICS
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40, pulse_style="bright_cyan"),
            transient=True,
        ) as progress:
            
            task1 = progress.add_task("[cyan]Initializing Core Registry...", total=100)
            task2 = progress.add_task("[magenta]Loading Neural Weights...", total=100)
            task3 = progress.add_task("[yellow]Synchronizing Uplink...", total=100)

            # Step-by-step fake 'loading' for aesthetic feel
            while not progress.finished:
                progress.update(task1, advance=2)
                if progress.tasks[0].percentage > 40: progress.update(task2, advance=3)
                if progress.tasks[1].percentage > 30: progress.update(task3, advance=5)
                time.sleep(0.03)

    # 3. FINAL HEALTH CHECK (Real Data)
    h = get_project_health()
    if h["score"] < 70:
        console.print(Panel(
            f"[bold red]⚠️  SYSTEM INTEGRITY ALERT: {h['score']}%[/]\n[yellow]Reason: {h['msg']}[/]",
            title="[bold red]PRE-FLIGHT DIAGNOSTIC[/]", border_style="red"
        ))
        console.print("\n[bold cyan][?] AUTO-REPAIR RECOMMENDED[/bold cyan]")
        fix = input("Would you like me to attempt an Auto-Repair (Harden) now? (y/n): ").lower()
        if fix == 'y':
            harden_environment()
        else:
            log_system_event(f"Startup Health Alert: {h['status']} (User ignored fix)", level="WARNING")
    else:
        console.print(Align.center(f"[bold green]✅ SYSTEM NOMINAL: {h['score']}% INTEGRITY VERIFIED[/]"))
        time.sleep(0.8)
    
    # Final buffer purge to ensure input is fresh for the main menu
    clear_keyboard_buffer()

def main():
    """
    PURPOSE: This is the heart of the switcher. 
    It is wrapped in a 'Global Crash Guard' to ensure the launcher stays alive even if something fails.
    """
    global IS_ADMIN
    IS_ADMIN = is_admin() # Cache for whole session
    
    # Pillar 7: Stealth Lockdown
    hide_file(LOG_FILE)
    hide_file(SETTINGS_FILE)
    
    # Start Background Connectivity Guard
    t = threading.Thread(target=connectivity_guard, daemon=True)
    t.start()

    # Step 1: Integrated Pre-flight Check (BOOT LOADER)
    boot_loader()

    # Clean up any leftover input
    clear_keyboard_buffer()

    # Pillar 5: Global Crash Guard
    # Variables for Dual-Speed refresh
    cached_health = None
    last_health_check = 0
    
    # Start the Cockpit Engine
    current_input = ""
    
    while True:
        try:
            # 💡 INTERACTIVE SENTINEL ENGINE (v3.7 - Immersive Fix)
            # Clear keyboard buffer to start fresh
            clear_keyboard_buffer() 
            
            # Use screen=True for the "Cockpit" feel and to prevent ghosting artifacts
            with Live(render_premium_menu(cached_health, current_input), console=console, refresh_per_second=10, screen=False, auto_refresh=True) as live:
                # Ensure we have fresh health data for the first render
                if not cached_health:
                    cached_health = get_project_health()
                    live.update(render_premium_menu(cached_health, current_input))
                
                while True: 
                    # 1. SLOW REFRESH (Health/Stats)
                    if time.time() - last_health_check > CONFIG["REFRESH_RATE_SLOW"]:
                        cached_health = get_project_health()
                        last_health_check = time.time()
                        live.update(render_premium_menu(cached_health, current_input))

                    # 2. FAST INPUT CAPTURE
                    has_input_change = False
                    key = None  # 🔥 FIX: reset key every loop
                    while msvcrt.kbhit():
                        try:
                            raw = msvcrt.getch()
                            
                            # Filter system artifacts (Escape sequences, function keys)
                            if raw == b'\x1b' or raw == b'\x00' or raw == b'\xe0':
                                time.sleep(0.01) # Small delay to see if more bytes arrive
                                clear_keyboard_buffer() 
                                continue
                            
                            key = raw.decode('utf-8', errors='ignore')
                            
                            if key in ['\r', '\n']: # Enter
                                break # Exit the input-burst while loop
                            elif key == '\x08': # Backspace
                                if len(current_input) > 0:
                                    current_input = current_input[:-1]
                                    has_input_change = True
                            elif key.isprintable() and ord(key) < 128:
                                # Standard ASCII Only
                                if len(current_input) < 40:
                                    current_input += key
                                    has_input_change = True
                        except Exception:
                            pass
                    
                    # Update UI if input changed
                    if has_input_change:
                        live.update(render_premium_menu(cached_health, current_input))

                    # Exit inner loop if Enter was pressed
                    if key in ['\r', '\n']:
                        break
                    
                    # Small sleep to prevent 100% CPU usage while waiting for input
                    time.sleep(0.02) 

            # Action Phase: Process captured choice
            choice = current_input.strip().lower()
            current_input = "" 
            
            if not choice:
                continue 

            # --- SUSPEND FOR COMMAND EXECUTION ---
            # Screen=True automatically restores the buffer on exit from 'with' block
            console.clear()

            # --- BLOCK 4: THE SWITCHBOARD (CHOOSING THE ACTION) ---
            
            # NLU COMMAND PARSER: Understanding basic human-like commands
            words = choice.split()
            help_patterns = ['help', '?', 'info', 'commands', 'h', 'guide']
            
            # Check for "help [topic]" or "[topic] help"
            is_help_request = any(w in help_patterns for w in words)
            
            if is_help_request:
                # Extract the topic (any word that is NOT a help pattern)
                topics = [w for w in words if w not in help_patterns]
                topic = topics[0] if topics else None
                show_help(topic)
                continue

            # ALIASING: mapping words to numbers
            cmd_map = {
                'run': '1', 'start': '1', 'launch': '1', 'dashboard': '1', 'webapp': '1',
                'ext': '2', 'external': '2',
                'jupyter': '3', 'notebook': '3',
                'harden': '5', 'setup': '5', 'install': '5', 'fix': '5',
                'github': '6', 'repo': '6',
                'venv': '7', 'switch': '7',
                'upgrade': '8', 'migrate': '8',
                'pull': '9', 'update': '9',
                'push': '10', 'commit': '10', 'sync': '10',
                'ignore': '11', 'gitignore': '11',
                'audit': '12', 'path': '12',
                'restart': '13', 'reload': '13',
                'stop': '14', 'exit': '14', 'bye': '14', 'quit': '14',
                'global': '15', 'cs': '15', 'register': '15',
                'reset': '16', 'clear_settings': '16',
                'alias': '17', 'bro': '17', 'cyber': '17', 'register_all': '17',
                'speed': '18', 'network': '18', 'test': '18', 'internet': '18',
                'help': '19', 'guide': '19', 'h': '19', 
                'log': '20', 'logs': '20', 'audit_logs': '20'
            }
            
            # SENSE: Natural Language Intent Routing
            matched_choice = None
            for word in words:
                if word in cmd_map:
                    if cmd_map[word] == '18':
                        matched_choice = '18'
                        break
                    if not matched_choice:
                        matched_choice = cmd_map[word]
            
            if matched_choice:
                choice = matched_choice

            # Check for Health Warning before launching (Option 1/2)
            h_score = cached_health["score"] if cached_health else get_project_health()["score"]
            if choice in ['1', '2'] and h_score < 50:
                print(f"\n{RED}[!] CAUTION: Health Score is low ({h_score}%).{RESET}")
                print(f"{YELLOW}[!] Launch may fail due to missing files or dependencies.{RESET}")
                confirm = input("[?] Proceed regardless? (y/n): ").lower()
                if confirm != 'y': continue

            if choice == '1':
                run_script("Start_WebApp_Venv.bat", new_window=False)

            elif choice == '2':
                run_script("Start_WebApp_Venv.bat", new_window=True)
                input("\n[!] External Process Started. Press ENTER to return to menu...")

            elif choice in ['3', 'jupyter', 'notebook']:
                run_script("Start_Jupyter_Venv.bat", new_window=False)

            elif choice == '4':
                run_script("Start_Jupyter_Venv.bat", new_window=True)
                input("\n[!] External Process Started. Press ENTER to return to menu...")

            elif choice in ['5', 'harden', 'setup', 'install']:
                harden_environment()

            elif choice in ['6', 'github', 'repo', 'source']:
                open_repo_smart()
                input("\n[!] Browser Spawned. Press ENTER to return to menu...")

            elif choice in ['7', 'venv', 'virtualenv', 'isolate']:
                # Pillar 4: Handoff Safety
                if IS_VIRTUAL:
                    print("[!] Already running in Virtual Environment.")
                    time.sleep(1)
                    continue
                
                venv_exe = os.path.join(root_dir, '.venv', 'Scripts', 'python.exe')
                if not os.path.exists(venv_exe):
                    print(f"[-] Error: Virtual Environment not found at {venv_exe}")
                    print("[!] Please use Option 5 (Harden) to rebuild the environment first.")
                    input("\nPress ENTER to continue...")
                    continue
                
                print(f"[*] Handoff to Venv: {venv_exe}")
                time.sleep(1)
                os.execl(venv_exe, venv_exe, *sys.argv)

            elif choice in ['8', 'upgrade']:
                if IS_VIRTUAL:
                    print("[!] Already running in Virtual Environment.")
                    time.sleep(1)
                    continue
                venv_exe = os.path.join(root_dir, '.venv', 'Scripts', 'python.exe')
                if os.path.exists(venv_exe):
                    print("[*] Environment Sync: Migrating to Virtual Environment...")
                    time.sleep(1)
                    os.execl(venv_exe, venv_exe, *sys.argv)
                else:
                    print("[-] No Virtual Environment found. Running Hardening Engine first...")
                    harden_environment()
                    if os.path.exists(venv_exe):
                        os.execl(venv_exe, venv_exe, *sys.argv)

            elif choice in ['9', 'pull', 'update']:
                print("\n[*] Pulling latest changes from repository...")
                try:
                    subprocess.run(["git", "pull"], cwd=root_dir, check=True)
                    print("\n[+] Git Pull Complete.")
                except Exception as e:
                    print(f"\n[-] Git Error: {e}")
                    print("[!] Ensure Git is installed and you have an internet connection.")
                input("\nPress ENTER to return to menu...")

            elif choice in ['10', 'push', 'commit', 'sync', 'upload']:
                commit_msg = input("\n[?] Enter commit message (or press ENTER to cancel): ").strip()
                if commit_msg:
                    try:
                        print("[*] Staging all files (git add .)...")
                        subprocess.run(["git", "add", "."], cwd=root_dir, check=True)
                        print(f"[*] Committing as: '{commit_msg}'...")
                        subprocess.run(["git", "commit", "-m", commit_msg], cwd=root_dir, check=True)
                        print("[*] Pushing to repository (git push)...")
                        subprocess.run(["git", "push"], cwd=root_dir, check=True)
                        print("\n[+] Git Operations Successful!")
                    except Exception as e:
                        print(f"\n[-] Git Sync failed: {e}")
                        log_system_event(f"Git Sync Error: {e}", level="ERROR")
                else:
                    print("[-] Operation Canceled.")
                input("\nPress ENTER to return to menu...")

            elif choice in ['11', 'ignore', 'gitignore']:
                gitignore_path = os.path.join(root_dir, ".gitignore")
                print(f"\n{BOLD_CYAN}--- GIT IGNORE MANAGER ---{RESET}")
                print("1. [Manual] Add specific file/folder name")
                print("2. [Automatic] Add current folder to ignore")
                print("3. [Harden] Add all common development patterns")
                print("C. Cancel")
                
                sub_choice = input(f"\n{YELLOW}[?] Select mode: {RESET}").lower()
                
                to_add = []
                if sub_choice == '1':
                    manual_path = input(f"{YELLOW}[?] Enter file/folder to ignore: {RESET}").strip()
                    if manual_path: to_add.append(manual_path)
                elif sub_choice == '2':
                    folder_name = os.path.basename(root_dir)
                    to_add.append(f"{folder_name}/")
                elif sub_choice == '3':
                    to_add = ["*.log", "launcher_debug.log", ".venv/", "__pycache__/", "*.pyc", ".vscode/", "Project materials/"]
                
                if to_add:
                    try:
                        existing = []
                        if os.path.exists(gitignore_path):
                            with open(gitignore_path, "r") as f:
                                existing = [line.strip() for line in f.readlines()]
                        
                        added_count = 0
                        with open(gitignore_path, "a") as f:
                            for p in to_add:
                                if p not in existing:
                                    f.write(f"{p}\n")
                                    added_count += 1
                                    print(f"{GREEN}[+] Added to ignore: {p}{RESET}")
                        
                        if added_count == 0:
                            print(f"{YELLOW}[!] All entries were already in .gitignore.{RESET}")
                        else:
                            log_system_event(f"Git Protection: Added {added_count} items.", level="INFO")
                        
                    except Exception as e:
                        print(f"{RED}[-] Error: {e}{RESET}")
                else:
                    print("[-] No changes made.")
                input("\nPress ENTER to return to menu...")

            elif choice in ['12', 'audit', 'diagnostic']:
                check_system_paths()

            elif choice in ['13', 'restart', 'reload']:
                print("[*] Synchronizing Environment for Restart...")
                # Pillar 1: Professional Safe Exit before Handoff
                if 'live' in locals() and live.is_started:
                    live.stop()
                
                # Pillar 5: Zero-Failure Process Handoff
                # On Windows, os.execl is replaced by spawnl + exit.
                # We need to ensure the console is flushed and ready.
                sys.stdout.flush()
                sys.stderr.flush()
                time.sleep(1.0) # Wait for terminal to settle
                
                try:
                    # Use absolute path to python for reliability
                    python_exe = sys.executable
                    subprocess.Popen([sys.executable, os.path.abspath(__file__)])
                    sys.exit()
                except Exception as restart_err:
                    print(f"[-] Restart failed: {restart_err}")
                    input("Press ENTER to return to menu...")

            elif choice in ['14', 'exit', 'bye', 'stop']:
                print(f"\n{GREEN}[*] Goodbye! Secure logout complete.{RESET}")
                return

            elif choice in ['15', 'global', 'cs', 'register']:
                setup_global_access("cs")
                
            elif choice in ['16', 'reset', 'clear_settings']:
                settings = load_settings()
                settings["browser_mode"] = None
                settings["turbo_mode"] = False
                save_settings(settings)
                print(f"\n{GREEN}[+] All launcher preferences cleared.{RESET}")
                input("Press ENTER to return to menu...")

            elif choice in ['17', 'alias', 'bro', 'cyber']:
                setup_all_aliases()

            elif choice in ['18', 'speed', 'network', 'test']:
                run_speed_test()

            elif choice in ['19', 'help', 'guide']:
                show_help()

            elif choice in ['20', 'log', 'logs']:
                print("[*] Launching Live Audit Logs (External)...")
                subprocess.Popen(['notepad.exe', LOG_FILE])

            # --- RESUME PHASE ---
            # After command exits, we clear the console.
            # The next iteration of the main loop will restart the Live engine automatically.
            console.clear()
            # Give the terminal half a second to settle focus and buffer switches
            time.sleep(0.5)
            # Drain any leftover characters from command inputs (like Git commit msgs)
            clear_keyboard_buffer()

        except KeyboardInterrupt:
            # Pillar 1: Professional Safe Exit on Ctrl+C
            print("\n\n[*] Safe Exit Triggered. Goodbye!")
            sys.exit(0)
            
        except Exception as e:
            # Pillar 5: Master Catch-All UI
            # NEW: AI AUTO-DIAGNOSIS
            error_msg = str(e).lower()
            advice = "Please check launcher_debug.log for technical details."
            
            if "not found" in error_msg:
                advice = "A required program (Git, Python, or a dependency) is missing. Try Option 5."
            elif "access is denied" in error_msg or "perm" in error_msg:
                advice = "Permission error! Please restart the launcher as ADMINISTRATOR."
            elif "disk" in error_msg or "space" in error_msg:
                advice = "Your computer's storage is full. Please clear some space."

            log_system_event(f"MASTER ENGINE CRASH: {str(e)}", level="CRITICAL")
            print("\n" + f"{RED}" + "="*45 + f"{RESET}")
            print(f" {RED}[CRITICAL SYSTEM ERROR CAUGHT]{RESET} ")
            print(f" Error: {e}") 
            print(f" {YELLOW}[AI ADVICE]: {advice}{RESET}")
            print(f"{RED}" + "="*45 + f"{RESET}")
            
            # gc.collect(): MEMORY FIX - Clears internal Python 'junk' before restarting.
            gc.collect() 
            input(f"\n{YELLOW}[RECOVERED] Press ENTER to restart the menu engine...{RESET}")



# This special condition makes sure main() only runs if you double-click THIS file.
# If another script tries to 'import' this file, it won't start the menu automatically.
if __name__ == "__main__":
    main()

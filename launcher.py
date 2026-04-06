import subprocess
import os
import sys

def run_script(script_name, new_window=False):
    """
    Executes a local .bat script. Supports Integrated and External modes.
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(root_dir, script_name)

    if not os.path.exists(script_path):
        print(f"[-] Error: Script '{script_name}' not found.")
        return

    mode_label = "NEW TERMINAL" if new_window else "INTEGRATED"
    print(f"[+] Launching CyberShield Engine ({mode_label})")
    print(f"[+] Script: {script_name}")
    print("--------------------------------------------------")
    
    try:
        if new_window:
            # Use 'start' to spawn a new CMD window and run the script
            # '/k' keeps the window open even if the script finishes
            subprocess.Popen(['start', 'cmd', '/k', script_path], shell=True)
            print("[*] Process spawned in separate window successully.")
        else:
            # Runs in the current terminal (standard integrated mode)
            subprocess.run([script_path], shell=True, check=True)
    except KeyboardInterrupt:
        print("\n[!] Launcher: Process interrupted.")
    except Exception as e:
        print(f"\n[-] Launcher: Error: {e}")

def main():
    while True:
        # Professional clear screen for menu persistence
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==========================================")
        print("   CyberShield AI - COMMAND CENTER       ")
        print("==========================================")
        print("1. Launch Dashboard (Integrated - Same Window)")
        print("2. Launch Dashboard (External - New Window)")
        print("3. Launch Jupyter   (Integrated - Same Window)")
        print("4. Launch Jupyter   (External - New Window)")
        print("5. Exit Launcher")
        print("------------------------------------------")

        choice = input("Selection Code (1-5): ").strip()

        if choice == '1':
            run_script("Start_WebApp_Venv.bat", new_window=False)
        elif choice == '2':
            run_script("Start_WebApp_Venv.bat", new_window=True)
            input("\n[!] External Process Started. Press ENTER to return to menu...")
        elif choice == '3':
            run_script("Start_Jupyter_Venv.bat", new_window=False)
        elif choice == '4':
            run_script("Start_Jupyter_Venv.bat", new_window=True)
            input("\n[!] External Process Started. Press ENTER to return to menu...")
        elif choice == '5':
            print("[*] Closing Command Center.")
            break
        else:
            print("[-] Invalid code.")
            input("Press ENTER to retry...")

if __name__ == "__main__":
    main()

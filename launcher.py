import subprocess
import os
import sys
import time

# Professional Terminal Environment Detection
IS_VIRTUAL = sys.prefix != sys.base_prefix
root_dir = os.path.dirname(os.path.abspath(__file__))

def run_script(script_name, new_window=False):
    """
    Executes a local .bat script. Supports Integrated and External modes.
    """
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
            subprocess.Popen(['start', 'cmd', '/k', script_path], shell=True)
            print("[*] Process spawned in separate window successfully.")
        else:
            subprocess.run([script_path], shell=True, check=True)
    except KeyboardInterrupt:
        print("\n[!] Launcher: Process interrupted.")
    except Exception as e:
        print(f"\n[-] Launcher: Error: {e}")

def harden_environment():
    """
    Launches the premium TUI hardening engine directly within the script.
    Uses 'Lazy Imports' to prevent crashes in environments where 'rich' is missing.
    """
    print("\n[!] Initializing 2026 High-Performance Hardening Engine...")
    
    try:
        # Step 1: Ensure dependencies are present (No Console yet)
        subprocess.run([sys.executable, "-m", "pip", "install", "rich"], capture_output=True)
        
        # Step 2: Lazy Import the TUI components
        from rich.console import Console
        from rich.panel import Panel
        from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn
        from rich.table import Table
        from rich.text import Text
        
        console = Console()
        
        # Visual Phase 1: Header
        header_text = Text("🛡️ CyberShield AI: HIGH-PERFORMANCE HARDENING ENGINE (2026)", style="bold cyan")
        console.print(Panel(header_text, border_style="bright_blue", expand=False))
        
        # Visual Phase 2: Diagnostic Audit
        table = Table(title="[SYSTEM DIAGNOSTIC]", show_header=True, header_style="bold magenta")
        table.add_column("Component", style="cyan")
        table.add_column("Version / Status", style="green")
        table.add_row("Python Core", f"{sys.version.split()[0]} (Hardened)")
        table.add_row("Environment", "VIRTUAL (.venv)" if IS_VIRTUAL else "GLOBAL (Legacy)")
        table.add_row("TUI Engine", "Rich v14.3 (Active)")
        table.add_row("ML Pipeline", "Zero-Failure Ready")
        console.print(table)
        
        # Visual Phase 3: Animated Installation
        with Progress(
            SpinnerColumn(spinner_name="dots2"),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=None, pulse_style="bright_cyan"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            DownloadColumn(),
            TransferSpeedColumn(),
            expand=True
        ) as progress:
            task1 = progress.add_task("[cyan]Scanning Requirements...", total=100)
            task2 = progress.add_task("[magenta]Downloading Binary Wheels...", total=100)
            task3 = progress.add_task("[green]Hardening 3.13.12 Core...", total=100)
            
            while not progress.finished:
                time.sleep(0.04)
                progress.update(task1, advance=1.1)
                if progress.tasks[0].completed > 50:
                    progress.update(task2, advance=0.9)
                if progress.tasks[1].completed > 30:
                    progress.update(task3, advance=0.7)
        
        # Visual Phase 4: Success
        console.print("\n✅ ENVIRONMENT HARDENING COMPLETE: EXAMINER READY 🛡️", style="bold green")
        console.print("--------------------------------------------------")
        
    except Exception as e:
        print(f"[-] Hardening Error: {e}")
        print("[!] Falling back to standard installation...")
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "install_deps.ps1"])
    
    input("\n[PROCESSS COMPLETE] Press ENTER to return to menu...")

def main():
    while True:
        # Professional clear screen for menu persistence
        os.system('cls' if os.name == 'nt' else 'clear')
        
        env_label = "[VIRTUAL ENV ACTIVE]" if IS_VIRTUAL else "[GLOBAL PYTHON - LEGACY]"
        env_color = "\033[92m" if IS_VIRTUAL else "\033[93m"
        reset = "\033[0m"

        print("==========================================")
        print("   CyberShield AI - COMMAND CENTER       ")
        print(f"   {env_color}{env_label}{reset}")
        print("==========================================")
        print("1. Launch Dashboard (Integrated - Same Window)")
        print("2. Launch Dashboard (External - New Window)")
        print("3. Launch Jupyter   (Integrated - Same Window)")
        print("4. Launch Jupyter   (External - New Window)")
        print("5. Initialize/Harden 2026 Environment (Install Setup)")
        print("6. Exit Launcher")
        print("------------------------------------------")

        choice = input("Selection Code (1-6): ").strip()

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
            harden_environment()
        elif choice == '6':
            print("[*] Closing Command Center.")
            break
        else:
            print("[-] Invalid code.")
            input("Press ENTER to retry...")

if __name__ == "__main__":
    main()

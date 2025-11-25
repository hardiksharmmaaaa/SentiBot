import os
import subprocess
import sys
import time

def main():
    """
    Sets up the environment and runs the sentiment chatbot application.
    """
    base_dir = os.path.dirname(__file__)
    backend_dir = os.path.join(base_dir, 'backend')
    frontend_dir = os.path.join(base_dir, 'frontend-react')
    
    # --- Backend Setup ---
    print("--- Setting up Backend ---")
    
    # Create a virtual environment
    venv_dir = os.path.join(backend_dir, 'venv')
    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, '-m', 'venv', venv_dir])

    # Determine the path to the Python executable in the venv
    if sys.platform == 'win32':
        python_executable = os.path.join(venv_dir, 'Scripts', 'python.exe')
    else:
        python_executable = os.path.join(venv_dir, 'bin', 'python')

    # Install dependencies
    print("Installing backend dependencies...")
    subprocess.check_call([
        python_executable, '-m', 'pip', 'install', '-r',
        os.path.join(backend_dir, 'requirements.txt')
    ])

    # Start the Flask application in the background
    print("Starting the backend server...")
    backend_process = subprocess.Popen([
        python_executable,
        os.path.join(backend_dir, 'app', 'main.py')
    ])
    
    print("Backend server started at http://127.0.0.1:5001")

    # --- Frontend Setup ---
    print("\n--- Setting up Frontend ---")
    
    # Check if node_modules exists, if not install
    if not os.path.exists(os.path.join(frontend_dir, 'node_modules')):
        print("Installing frontend dependencies (this may take a while)...")
        subprocess.check_call(['npm', 'install'], cwd=frontend_dir)
    else:
        print("Frontend dependencies already installed.")

    # Start the React application
    print("Starting the frontend application...")
    try:
        subprocess.check_call(['npm', 'start'], cwd=frontend_dir)
    except KeyboardInterrupt:
        print("\nStopping application...")
        backend_process.terminate()
        sys.exit(0)

if __name__ == '__main__':
    main()
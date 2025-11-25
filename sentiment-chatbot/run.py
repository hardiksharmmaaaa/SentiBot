import os
import subprocess
import sys

def main():
    """
    Sets up the environment and runs the sentiment chatbot application.
    """
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    
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
    print("Installing dependencies...")
    subprocess.check_call([
        python_executable, '-m', 'pip', 'install', '-r',
        os.path.join(backend_dir, 'requirements.txt')
    ])

    # Run the Flask application
    print("Starting the backend server...")
    subprocess.Popen([
        python_executable,
        os.path.join(backend_dir, 'app', 'main.py')
    ])

    print("\nBackend server is running.")
    print("You can now open http://localhost:8000 in your browser.")

    # Start a simple HTTP server for the frontend
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    os.chdir(frontend_dir)
    
    import http.server
    import socketserver

    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

if __name__ == '__main__':
    main()
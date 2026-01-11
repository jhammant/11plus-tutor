#!/usr/bin/env python3
"""
Start ExamTutor Application
Launches both backend (FastAPI) and frontend (Next.js)
"""

import subprocess
import sys
import os
import time
import signal
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = PROJECT_ROOT / "src" / "api"
FRONTEND_DIR = PROJECT_ROOT / "web"

# Ports (different from AIEducator which uses 8001/3782)
BACKEND_PORT = 8002
FRONTEND_PORT = 3783

# Process handles
processes = []


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\nShutting down...")
    for p in processes:
        try:
            p.terminate()
            p.wait(timeout=5)
        except:
            p.kill()
    sys.exit(0)


def check_port(port):
    """Check if a port is available"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0


def start_backend():
    """Start the FastAPI backend"""
    print(f"Starting backend on port {BACKEND_PORT}...")

    if not check_port(BACKEND_PORT):
        print(f"  Warning: Port {BACKEND_PORT} is already in use")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)

    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.api.main:app",
         "--host", "0.0.0.0",
         "--port", str(BACKEND_PORT),
         "--reload"],
        cwd=PROJECT_ROOT,
        env=env,
    )
    processes.append(process)
    return process


def start_frontend():
    """Start the Next.js frontend"""
    print(f"Starting frontend on port {FRONTEND_PORT}...")

    if not check_port(FRONTEND_PORT):
        print(f"  Warning: Port {FRONTEND_PORT} is already in use")

    # Check if node_modules exists
    if not (FRONTEND_DIR / "node_modules").exists():
        print("  Installing frontend dependencies...")
        subprocess.run(["npm", "install"], cwd=FRONTEND_DIR, check=True)

    env = os.environ.copy()
    env["PORT"] = str(FRONTEND_PORT)

    process = subprocess.Popen(
        ["npm", "run", "dev", "--", "-p", str(FRONTEND_PORT)],
        cwd=FRONTEND_DIR,
        env=env,
    )
    processes.append(process)
    return process


def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                              ExamTutor                                       ║
║                   AI-Powered UK Exam Preparation                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Initialize database and import questions
    print("Initializing database...")
    sys.path.insert(0, str(PROJECT_ROOT))
    from src.core.database import init_db, Question, SessionLocal
    init_db()

    # Check if questions need to be imported
    db = SessionLocal()
    question_count = db.query(Question).count()
    db.close()

    if question_count < 100:
        print(f"  Found only {question_count} questions, importing full question bank...")
        from scripts.import_questions import import_all_questions
        import_all_questions()
    else:
        print(f"  Database ready: {question_count} questions available")

    # Start services
    backend = start_backend()
    time.sleep(2)  # Give backend time to start
    frontend = start_frontend()

    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  Services Started:                                                           ║
║  ─────────────────────────────────────────────────────────────────────────── ║
║  Frontend:  http://localhost:{FRONTEND_PORT}                                       ║
║  Backend:   http://localhost:{BACKEND_PORT}                                        ║
║  API Docs:  http://localhost:{BACKEND_PORT}/docs                                   ║
║                                                                              ║
║  Press Ctrl+C to stop                                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

    # Wait for processes
    try:
        while True:
            # Check if processes are still running
            if backend.poll() is not None:
                print("Backend stopped unexpectedly!")
                break
            if frontend.poll() is not None:
                print("Frontend stopped unexpectedly!")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)


if __name__ == "__main__":
    main()

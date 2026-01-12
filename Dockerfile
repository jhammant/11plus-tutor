# 11+ Tutor Application Docker Container
# Runs both FastAPI backend and Next.js frontend

FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Install system dependencies and Node.js
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend package files for npm install caching
COPY web/package*.json ./web/

# Install frontend dependencies
WORKDIR /app/web
RUN npm install

# Copy the rest of the application
WORKDIR /app
COPY . .

# Create data directory for SQLite database
RUN mkdir -p /app/data

# Expose ports for frontend and backend
EXPOSE 3783 8002

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "Starting 11+ Tutor Application..."\n\
\n\
# Create .env.local for Next.js\n\
echo "NEXT_PUBLIC_API_BASE=http://localhost:8002" > /app/web/.env.local\n\
\n\
# Initialize database and start backend in background\n\
cd /app\n\
python -c "\n\
import sys\n\
sys.path.insert(0, \"/app\")\n\
from src.core.database import init_db, Question, SessionLocal\n\
init_db()\n\
db = SessionLocal()\n\
count = db.query(Question).count()\n\
db.close()\n\
if count < 100:\n\
    print(f\"Importing questions...\")\n\
    from scripts.import_questions import import_all_questions\n\
    import_all_questions()\n\
else:\n\
    print(f\"Database ready: {count} questions\")\n\
"\n\
\n\
# Start backend\n\
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8002 &\n\
\n\
# Wait for backend to be ready\n\
sleep 3\n\
\n\
# Start frontend\n\
cd /app/web\n\
npm run dev -- -p 3783 -H 0.0.0.0\n\
' > /app/start.sh && chmod +x /app/start.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:3783 || exit 1

# Run the application
CMD ["/app/start.sh"]

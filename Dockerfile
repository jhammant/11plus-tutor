# 11+ Tutor - Docker Setup
# Build: docker build -t 11plus-tutor .
# Run: docker run -p 3783:3783 -p 8002:8002 11plus-tutor

FROM python:3.12-slim

# Install Node.js
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend and install dependencies
COPY web/package*.json web/
RUN cd web && npm install

# Copy the rest of the application
COPY . .

# Build frontend
RUN cd web && npm run build

# Expose ports
EXPOSE 3783 8002

# Create startup script
RUN echo '#!/bin/bash\n\
cd /app\n\
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8002 &\n\
cd web && npm start\n\
' > /start.sh && chmod +x /start.sh

# Environment variables
ENV NEXT_PUBLIC_API_BASE=http://localhost:8002
ENV NODE_ENV=production

CMD ["/start.sh"]

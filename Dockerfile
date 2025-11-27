FROM python:3.11-slim

WORKDIR /app

# Install Node.js and Yarn for frontend
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g yarn \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy frontend code
COPY frontend/ ./frontend/

# Build frontend
WORKDIR /app/frontend
RUN yarn install && yarn build

WORKDIR /app

# Create data directory
RUN mkdir -p /app/data

# Copy built frontend to be served by FastAPI
RUN cp -r frontend/dist ./static

# Expose port
EXPOSE 8000

ENV DB_PATH=/app/data/subkeeper.db
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

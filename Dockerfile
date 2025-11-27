# =================================================================
# STAGE 1: Build Frontend Assets
#
# We use a Node.js image to install dependencies and build the
# frontend static files. We name this stage "builder".
# =================================================================
FROM node:22-slim AS builder

WORKDIR /app/frontend

# Copy package.json and install dependencies first to leverage Docker cache
COPY frontend/package*.json ./
RUN npm install

# Copy the rest of the frontend source code
COPY frontend/ ./

# Build the production-ready static files
RUN npm run build

# =================================================================
# STAGE 2: Final Production Image
#
# We start from a clean Python image. This will be our final image.
# It will NOT contain Node.js, npm, or any frontend source code.
# =================================================================
FROM python:3.11-slim

WORKDIR /app

# Install backend dependencies
# Copy only the requirements file first to leverage cache
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY backend/ .

# The magic step: Copy ONLY the built assets from the "builder" stage
# This copies the content of /app/frontend/dist from the "builder" stage
# into the /app/static directory in our final image.
COPY --from=builder /app/frontend/dist ./static

# Create data directory
RUN mkdir -p /app/data

# Expose port and set environment variables
EXPOSE 8000
ENV DB_PATH=/app/data/subkeeper.db
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
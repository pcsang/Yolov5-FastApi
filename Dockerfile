# Base image with Python and pip
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Download torch hub cache
RUN python -c "import torch; torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)"

# Expose the port
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

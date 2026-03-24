# Use a small, official Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first — Docker caches this layer
# so it won't re-run pip install unless requirements.txt changes
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Start the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
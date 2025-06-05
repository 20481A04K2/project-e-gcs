FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy source code
COPY . /app

# Install dependencies (Flask, requests, boto3 for AWS SQS)
RUN pip install --no-cache-dir Flask requests boto3

# Expose port 8080
EXPOSE 8080

# Run the Flask app
CMD ["python3", "app.py"]

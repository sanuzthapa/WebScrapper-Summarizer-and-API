# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install early for cache
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy app code and start script
COPY . .

# Make sure the script is executable
RUN chmod +x start.sh

# Expose both ports
EXPOSE 80
EXPOSE 8081

# Start both apps
CMD ["./start.sh"]

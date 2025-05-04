# Use the official Python 3.12 slim image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install the dependencies
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files (app.py and templates)
COPY app.py .
COPY templates/index.html templates/
COPY .env .

# Expose port 5000 for Flask
EXPOSE 5000

# Run the application when the container starts
CMD ["python", "app.py"]

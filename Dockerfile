# Use an official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the contents of the current directory into the container's /app directory
COPY . /app

# Upgrade pip before using it
RUN pip install --upgrade pip

# Install the Python packages listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# The Flask app listens on port 5000 inside the container
EXPOSE 5000

# Start the app when the container starts
CMD ["python", "app.py"]

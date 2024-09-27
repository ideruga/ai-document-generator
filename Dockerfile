# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose port (if your Flask app runs on port 5000)
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Copy the .env.example to .env inside the container (if you want to provide default values)
# If not, you can set the environment variables directly in the Dockerfile or at runtime
# COPY .env.example .env

# Command to run the application
CMD ["flask", "run"]

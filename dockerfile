# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . . 

# Expose port 80 for the application
EXPOSE 80

# Define environment variable

# Run app.py when the container launches
CMD ["uvicorn", "test:app", "--host", "0.0.0.0", "--port", "80"]

# Use the official Python image as the base image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 80 for the FastAPI app
EXPOSE 80

# Start the FastAPI app
CMD ["uvicorn", "test:app", "--host", "0.0.0.0", "--port", "80"]

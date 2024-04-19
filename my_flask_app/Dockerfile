# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Expose the port that Flask is running on
EXPOSE 5000

# Define environment variables
ENV MONGO_HOST=localhost
ENV MONGO_PORT=27017

# Run pytest for unit tests
RUN pytest

# Run the Flask application when the container launches
CMD ["python", "app/main.py"]

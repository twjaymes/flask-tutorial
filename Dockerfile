# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies and Rust
RUN apt-get update && \
    apt-get install -y curl build-essential && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    export PATH=/root/.cargo/bin:$PATH && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure Rust is available in the PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=run.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
# Use an official Python runtime as a base image
FROM python:3.11.7

# Set the working directory in the container
WORKDIR /server

# Copy the current directory contents into the container at /app
COPY . /server

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run server.py with uvicorn when the container launches
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]

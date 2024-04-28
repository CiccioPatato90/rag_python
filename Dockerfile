# Use a Python base image
FROM python:3.12.1

# Set the working directory inside the container
WORKDIR /app

# Copy the FastAPI server code to the container
COPY proxy_server.py .

# Install FastAPI and other dependencies
RUN pip install fastapi uvicorn websockets requests

# Command to run the FastAPI server
CMD ["uvicorn", "proxy_server:app", "--host", "0.0.0.0", "--port", "8000"]

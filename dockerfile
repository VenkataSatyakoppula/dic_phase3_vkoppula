# Stage 1: Building the FastAPI backend
FROM python:3.11 AS backend

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY ./backend/requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY ./backend /app

# Command to run on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Stage 2: Setting up the PHP frontend
FROM php:7.4-apache AS frontend

# Copy frontend code to the web server root
COPY ./dic_frontend /var/www/html

# Expose port 80 to access the PHP server
EXPOSE 80

# When using Docker Compose, you can set up a service for each of these stages
# and use a shared network to allow them to communicate with each other.


# Use an official, lightweight Python runtime as a parent image
FROM python:3.11-slim

# Set system environment variables to optimize Python within Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your web application code into the container
COPY app.py .

# Expose the default network port Streamlit uses
EXPOSE 8501

# Configure Streamlit behavior parameters and launch the web server
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]


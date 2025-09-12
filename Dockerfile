# Use official Python 3.13 image as base
FROM python:3.13-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements.txt and install dependencies first (better cache)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose port if your app uses one (optional, since desktop app mostly local)
# EXPOSE 8080

# Command to run your app (adjust if you want to run main.py directly)
CMD ["python", "main.py"]

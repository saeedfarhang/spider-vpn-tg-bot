# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables to ensure Python behaves as expected
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . /app/

# Expose the necessary port (if applicable)
# EXPOSE 8000

# Run the bot
CMD ["python", "main.py"]

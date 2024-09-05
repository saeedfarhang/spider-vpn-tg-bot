# Use the official Python image as a base for dependencies
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends 

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . /app/

# Use a lightweight final image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy only the necessary files from the builder stage
COPY --from=builder /app /app


COPY --from=builder /root/.local /root/.local

# Update PATH environment variable
ENV PATH=/root/.local/bin:$PATH

# Expose the necessary port (if applicable)
EXPOSE 8009

# Run the bot
CMD ["python", "main.py"]

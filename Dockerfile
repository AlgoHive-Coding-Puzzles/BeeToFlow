FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install git for cloning Hivecraft repository
RUN apt-get update && apt-get install -y git && apt-get clean

# Copy necessary files
COPY entrypoint.py /app/entrypoint.py

# Make the script executable
RUN chmod +x /app/entrypoint.py

# Set the entry point with arguments from action.yml
ENTRYPOINT ["python", "/app/entrypoint.py"]

# Stage 1: Base
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy files
COPY main.py requirements.txt ./

# Set environment variables
ENV PORT 8080
ENV PYTHONUNBUFFERED True

# Install production dependencies.
RUN pip install -r requirements.txt

# Set default command
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}

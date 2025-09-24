FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY pyproject.toml ./
COPY uv.lock ./
RUN uv sync --frozen

# Copy application code
COPY app/ ./app/

# Expose the port that Gradio runs on
EXPOSE 7860

# Set environment variables
ENV PYTHONPATH=/app
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860

# Run the application
CMD ["uv", "run", "python", "app/main.py"]
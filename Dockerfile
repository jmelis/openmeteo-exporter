FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set working directory
WORKDIR /app

# Enable bytecode compilation for faster imports
ENV UV_COMPILE_BYTECODE=1

# Copy dependency files first for better layer caching
COPY pyproject.toml ./

# Install dependencies using uv (system-wide, no virtual env needed in container)
RUN uv pip install --system --no-cache \
    prometheus-client>=0.19.0 \
    requests>=2.31.0 \
    pyyaml>=6.0.1

# Copy application files
COPY exporter.py ./

# Create config directory
RUN mkdir -p /config

# Expose metrics port (can be overridden by config)
EXPOSE 9091

# Run the exporter
CMD ["python3", "exporter.py"]

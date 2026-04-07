FROM python:3.10-slim

# Configure for Hugging Face Spaces (non-root run)
RUN useradd -m -u 1000 user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR /app

# Copy all files and configure permissions
COPY --chown=user:user . /app
USER user

# Install pip packages locally
RUN pip install --no-cache-dir -e .
RUN pip install --no-cache-dir fastapi uvicorn pydantic openai

# OpenEnv convention says to start the FastAPI server on port 7860
EXPOSE 7860

# We start the environment serving at the root
CMD ["openenv", "serve", "env:SupportTriageEnv", "--port", "7860", "--host", "0.0.0.0"]

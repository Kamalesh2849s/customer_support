FROM python:3.10-slim

# Hugging Face Spaces requires running as a non-root user!
RUN useradd -m -u 1000 user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR /app

# Copy and give ownership to the user
COPY . /app
RUN chown -R user:user /app

USER user

# Install everything locally for this user
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir ./support_triage_env
RUN pip install --no-cache-dir fastapi uvicorn pydantic openai

# OpenEnv convention says to start the FastAPI server on port 7860
EXPOSE 7860

# We start the environment serving
WORKDIR /app/support_triage_env
CMD ["openenv", "serve", "env:SupportTriageEnv", "--port", "7860", "--host", "0.0.0.0"]

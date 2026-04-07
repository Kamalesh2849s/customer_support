FROM python:3.10-slim

WORKDIR /app

# Copy everything into the Docker container
COPY . /app

# Install the nested package
RUN pip install -e ./support_triage_env

# Install required packages for the proxy space
RUN pip install fastapi uvicorn pydantic openai

# OpenEnv convention says to start the FastAPI server on port 7860 for HF Spaces
EXPOSE 7860

# We start the environment serving
CMD ["openenv", "serve", "support_triage_env.env:SupportTriageEnv", "--port", "7860", "--host", "0.0.0.0"]

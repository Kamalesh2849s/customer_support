FROM python:3.10-slim

WORKDIR /app

COPY . /app
RUN pip install -e .
RUN pip install fastapi uvicorn pydantic

# OpenEnv convention says to start the FastAPI server on port 7860 for HF Spaces
EXPOSE 7860

CMD ["openenv", "serve", "env:SupportTriageEnv", "--port", "7860", "--host", "0.0.0.0"]

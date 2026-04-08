FROM python:3.10-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
RUN uv lock && uv sync

COPY . .

EXPOSE 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]

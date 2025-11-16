# build stage
FROM python:3.11-slim as builder
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential libpq-dev
COPY requirements.txt .
RUN pip wheel -r requirements.txt -w /wheels

# final
FROM python:3.11-slim
WORKDIR /app
RUN useradd -m appuser
COPY --from=builder /wheels /wheels
RUN pip install --no-index --find-links=/wheels -r requirements.txt
COPY ./app /app/app
COPY ./alembic /app/alembic
ENV PYTHONUNBUFFERED=1
USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]

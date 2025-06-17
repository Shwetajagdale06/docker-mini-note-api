# Stage 1: builder
FROM python:3.12-alpine AS builder
WORKDIR /install
COPY app/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: runtime
FROM python:3.12-alpine
WORKDIR /app
COPY --from=builder /install /usr/local
COPY app /app

RUN mkdir -p /logs
VOLUME ["/logs"]

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

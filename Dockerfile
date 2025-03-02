# Builder
FROM cgr.dev/chainguard/python:latest-dev AS builder
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /build

RUN python -m venv /build/venv
ENV PATH="/build/venv/bin:$PATH"

COPY . .
RUN pip install --no-cache-dir .

# Distroless
FROM cgr.dev/chainguard/python:latest
WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY --from=builder /build/venv /venv
ENV PATH="/venv/bin:$PATH"

ENTRYPOINT ["python", "-m", "healthchecker"]
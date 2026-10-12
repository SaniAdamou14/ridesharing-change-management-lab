FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /srv

FROM base AS deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM deps AS runtime
RUN useradd -m -u 10001 appuser
COPY app ./app
USER appuser
EXPOSE 8012
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8012/health')"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8012"]

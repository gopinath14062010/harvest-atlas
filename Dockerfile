# Harvest Atlas - container image (works on Hugging Face Spaces, Cloud Run,
# Koyeb, Fly.io, Render Docker, etc.)
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Non-root user (Hugging Face Docker Spaces require uid 1000)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 7860

# Single worker on purpose: the app keeps the selected field in process memory.
CMD ["sh", "-c", "gunicorn --workers 1 --threads 8 --timeout 300 --bind 0.0.0.0:${PORT} serve:app"]

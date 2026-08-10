FROM python:3.12-slim AS runtime


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

RUN useradd --create-home --uid 10001 appuser
WORKDIR /app


COPY app/ ./app/

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import os,urllib.request,sys; \
        sys.exit(0) if urllib.request.urlopen('http://127.0.0.1:'+os.environ.get('PORT','8000')+'/health', timeout=2).status==200 else sys.exit(1)"

CMD ["python", "-m", "app"]

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE = 1\
    PYTHONUNBUFFERED = 1 \
    PIP_NO_CACHE_DIR = 1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY devOpsAssignment/ .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

COPY runner.sh /runner.sh
RUN chmod +x /runner.sh
CMD ["/runner.sh"]


FROM python:3.12.3-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    postgresql-client \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./ /code

COPY ./gespar.crt ./gespar.key /etc/gespar/ssl/

# 
CMD ["gunicorn", "-w 4", "-k uvicorn.workers.UvicornWorker", "main:app", "--certfile /etc/gespar/ssl/gespar.crt", "--keyfile /etc/gespar/ssl/gespar.key", "--bind", "0.0.0.0:443"]
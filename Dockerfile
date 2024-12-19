FROM google/cloud-sdk

LABEL maintainer="kesmail@pdx.edu"

COPY . /app

WORKDIR /app

RUN apt-get update -y && apt-get install -y python3-pip python3-venv \
        && python3 -m venv /env && /env/bin/pip install --no-cache-dir -r requirements.txt

ENV PATH="/env/bin:$PATH"

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app


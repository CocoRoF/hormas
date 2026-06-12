FROM python:3.10.2

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y git

WORKDIR /code
RUN mkdir -p /code/staticfiles /code/media
RUN python3 -m pip install --upgrade pip setuptools
RUN useradd -M -s /bin/false cocorof || true
RUN mkdir -p /code && chown -R cocorof:cocorof /code && chmod -R 777 /code
ENV PYTHONPATH="/code/web/nlp_model:${PYTHONPATH}"

EXPOSE 8000

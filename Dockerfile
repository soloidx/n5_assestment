FROM python:3.8.16-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
&& apt-get install gcc libc-dev --no-install-recommends -y \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install --user --no-cache-dir -r /tmp/requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /app/wait
RUN chmod +x /app/wait

COPY docker/entrypoint.sh /app/entrypoint.sh
COPY . /app/

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh" ]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

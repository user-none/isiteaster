FROM alpine:latest AS build
WORKDIR /app

COPY ./requirements.txt .
COPY ./app/translations translations

RUN apk add --no-cache git python3 py3-pip

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir gunicorn

RUN pybabel compile -d translations

RUN pip3 uninstall -y pip setuptools packaging


FROM alpine:latest AS release
EXPOSE 80
WORKDIR /app

RUN apk add --no-cache python3

COPY ./config.py .
COPY ./app ./isiteaster
COPY --from=build /app/translations isiteaster/translations

COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

VOLUME /data

CMD ["gunicorn", "--bind", "0.0.0.0:80", "isiteaster:create_app()" ]


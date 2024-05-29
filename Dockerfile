FROM alpine:latest AS build
WORKDIR /build

COPY ./LICENSE ./README.md ./pyproject.toml .
COPY ./isiteaster ./isiteaster

RUN apk add --no-cache python3 py3-pip

# Create build env
RUN python3 -m venv ./.venv
ENV PATH="/build/.venv/bin:$PATH"
RUN pip3 install --no-cache-dir pdm setuptools Babel

# Build the whl distribution file
RUN pdm build

# Create the runtime env
RUN python3 -m venv /opt/pyenv
ENV PATH="/opt/pyenv/bin:$PATH"
RUN pip3 install --no-cache-dir gunicorn
RUN pip install ./dist/*.whl
RUN pip3 uninstall -y pip setuptools packaging


FROM alpine:latest AS release
EXPOSE 80

RUN apk add --no-cache python3
COPY --from=build /opt/pyenv /opt/pyenv
ENV PATH="/opt/pyenv/bin:$PATH"

CMD ["gunicorn", "--bind", "0.0.0.0:80", "isiteaster:create_app()" ]

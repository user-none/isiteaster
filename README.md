# isiteaster

Web App to tell you if it's Easter

# Setup and Run

## Setting up the local environment

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running locally for Debug

After setting up the venv, the Flask local testing server will be available.

```
source .venv/bin/activate
flask --debug -A app:create_app run
```

## Running with gunicorn

Unlike the Flask local testing server, `gunicorn` requires you to specify that
`create_app` is a function which it needs to run to get the app object.

```
gunicorn --bind 0.0.0.0:7999 'app:create_app()
```

## Docker

```
docker build . -t isiteaster
```

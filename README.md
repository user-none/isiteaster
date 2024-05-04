# isiteaster

Web App to tell you if it's Easter.


## When Is Easter

Easter day moves each year and is based on the full moon. The exact day
of Easter for a given year can be determined using a multi-step
[algorithm](https://en.wikipedia.org/wiki/Date_of_Easter).

# App Design

The application written in Python using Flask. It is a traditional web
app where the back end drives a templated front end.

If it's not Easter, the application will show a sad face and state
the date of the next Easter day. If it is Easter, the app will show
a happy face and state that it is Easter.

## 3rd Party Services

A few third party services
can be used if configured for the application to be more accurate and performant.

### IP Geo Location

The [ipgeolocation](https://ipgeolocation.io) will be used if an API key is configured
in order to determine visitor's timezone. Since the application is trying to inform
the visitor whether it is Easter, timezone needs to be taken into account.

If this service is not enabled, the app will use the server's timezone.

A few protections are in place to prevent unnecessary IP lookups.

1. If the IP is within an internal range lookup will be skipped and the server
   timezone will be used.
2. The user-agent is checked to prevent lookups for non-human visitors.
   A database of known bots and web crawlers is used try and identify
   these visitors.

### IP Timezone Caching

Flask-Cache is supposed and can be used to cache IP to timezone lookup results.
This further reduces lookups to the IP Geolocation service. Flask-Cache
supports a variety of back ends including caching servers such as Redis,
Memcached, or local file.

# Images

Images are not required to be provided. However, none are included
but, if provided, will be used when detected. If images are not present, an
alternative is used. Specially, if bunny pictures are not present, emoji
are used. If a favicon.ico is not present, a blank favicon.ico will be used.

- `static/images/bunny_happy.svg`: Picture of a happy bunny used when it is Easter
- `static/images/bunny_sad.svg`: Picture of a sad bunny used when it is _not_ Easter
- `static/favicon.ico`: Favicon.

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

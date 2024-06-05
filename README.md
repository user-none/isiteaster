# isiteaster

Web App to tell you if it's Easter.


## When Is Easter?

Easter day moves each year and is based on the full moon. The exact day
of Easter for a given year can be determined using a multi-step
[algorithm](https://en.wikipedia.org/wiki/Date_of_Easter).


# App Design

The application written in Python using Flask. It is a traditional web
app where the back end drives a templated front end.

If it's not Easter, the application will show a sad face and states
the day Easter will next fall on. If it's Easter, the app will show
a happy face and state that it's Easter.

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

Images are not required to be provided. However, none are included. If external
images are provided, they be used. External images are auto detected in order
for the application to know it should be used. If images are not present, an
alternative is used. Specially, if bunny pictures are not present, emoji are
used. If a `favicon.ico` is not present, a blank `favicon.ico` will be used.

## Image Files

- `bunny_happy.svg`: Picture of a happy bunny used when it is Easter
- `bunny_sad.svg`: Picture of a sad bunny used when it is _not_ Easter
- `favicon.ico`: Favicon.

## Image Location(s)

The default image location is `isiteaster/static/images/`. Images can be placed
in this directory or alternately, the configuration setting `IMAGE_DIR` can be
specified to use a different location for the above images. This allows the
images to be stored outside of the application.


# Configuration

There are three ways the application can be configured.

1. Editing the `config.py`. However, this isn't recommended and should be left
   as a default file.
2. Use an instance configured file. Create `instance/config.py` and set the settings
   within that file.
3. Use a config file referenced by the environment variable `ISITEASTER_CONF`. The file
   specified will be read and configuration settings applied.

Configuration files are stacked with 1-3 being read and applied. Meaning, a later file's value
will be used.

## Settings

### `REQUESTS_PROXIED`

boolean

Whether or not a reverse proxy is in use. When True will use the IP address
from the `X-Forwarded-For` header set by the reverse proxy. Otherwise, the IP
address of the client connection will be used.

### `IPGEO_API_KEY`

string

API key for the IP geo location service. If not set the service will not be used.

### `CACHE_CONFIG`

dict

Flask-Caching configuration.

### `IMAGE_DIR`

string

Directory on disk where images are located.


# Setup and Run

## Setting up the local environment

```zsh
python -m venv .venv
source .venv/bin/activate
pip install .
```

## Running locally for Debug

After setting up the venv, the Flask local testing server will be available.

```zsh
source .venv/bin/activate
flask --debug -A isiteaster:create_app run
```

## Running with gunicorn

Unlike the Flask local testing server, `gunicorn` requires you to specify that
`create_app` is a function which it needs to run to get the app object.

```zsh
gunicorn --bind 0.0.0.0:7999 'isiteaster:create_app()'
```

## Docker

All files related to the docker image are contained within the `docker` directory.
The Docker build needs to be run from the top level directory of the project.

```zsh
docker build . -t isiteaster -f docker/Dockerfile
```

### Data

The continuer uses the volume at `/data` for the base location of all files that
can be externally managed. The data directory is split into sub directories for
different functionality in order to allow different mount points to be used.

- `/data/conf/`
- `/data/images/`
- `/data/cache/`

#### /data/conf/

The application configuration file is `/data/conf/isiteaster.conf`.

#### /data/images/

The `IMAGE_DIR` parameter within the configuration file is set to `/data/images`.
Images as defined in the "Images" section should be mounted to this location.

#### /data/cache/

By default a file system cache is used to cache time zone offsets of IP address.
If this is mounted the cache can be persisted outside of Docker. Instead
of it managing cache data as part of a volume.


# Packaging

PDM can be used for building wheel a wheel and a non-DVCS source package.

```zsh
source .venv/bin/activate
pip install pdm setuptools
pdm build
```

Building with PDM will also compile `.po` translation files into `.mo` files.


# Translations

The application supports translations using Flask-Babel. Currently
English and Dutch are supported. There are no plans to support additional
languages at this time. Most likely any requests for additional languages
will be declined due to needing someone who is fluent to comment to keeping
the translations up to date in the future.

## Adding additional languages

1. Add the language code for the desired language to the list of supported languages in `isiteaster/utils/locale.py`.
2. Initialize the new language for adding translations with `pybabel init -i messages.pot -d isiteaster/translations -l <LANG_CODE>`.
3. Edit `isiteaster/translations/<LANG_CODE>/LC_MESSAGES/messages.po` and add the translations.
4. Compile the translations using `pybabel compile -d isiteaster/translations`

Where `<LANG_CODE>` is the language code. For example, `de`, or `es`.

## Adding new strings

All translatable strings should be either in the `j2` template and need
to be wrapped in `{{ _('') }}` or in a `py` file. When in a `py` file
`from flask_babel import gettext` and `gettext('')`.

## Updating translations after new strings are added

1. Generate new `messages.pot` file with the extracted strings using `pybabel extract -F babel.cfg -o messages.pot isiteaster`.
2. Merge the new strings into the translation `po` files using `pybabel update -i messages.pot -d isiteaster/translations`.
3. Edit all `po` files for each language located in `isiteaster/translations/<LANG_CODE>/LC_MESSAGES/messages.po`.
4. Compile the translations using `pybabel compile -d isiteaster/translations`.

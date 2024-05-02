# Copyright 2024 John Schember <john@nachtimwald.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import Flask, Blueprint
from flask_caching import Cache

cache = Cache()

def _load_config(app):
    app.config.from_object('config')
    app.config.from_pyfile('config.py', silent=True)

def _register_blueprints(app):
    from .routes import index
    app.register_blueprint(index.bp)
    from .routes import favicon
    app.register_blueprint(favicon.bp)

def _register_error_handlers(app):
    from .routes.error.e404 import page_not_found
    app.register_error_handler(404, page_not_found)
    from .routes.error.e500 import internal_server_error
    app.register_error_handler(500, internal_server_error)

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    _load_config(app)
    _register_blueprints(app)
    _register_error_handlers(app)

    cache.init_app(app, config=app.config.get('CACHE_CONFIG'))

    return app

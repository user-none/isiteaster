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

import os

from flask import Blueprint, send_from_directory, url_for, current_app

bp = Blueprint('favicon', __name__)

@bp.route('/favicon.ico')
def favicon():
    print(current_app.config['FAVICON'])
    return send_from_directory('static', current_app.config['FAVICON'], mimetype='image/vnd.microsoft.icon')

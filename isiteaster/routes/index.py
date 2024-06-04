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

from datetime import datetime

from flask import Blueprint, render_template, request, current_app

from ..utils.easter import when_is_easter

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    iseaster, easter = when_is_easter(request, current_app.config)
    return render_template('index.j2',
               iseaster=iseaster,
               easter_date=easter,
               bunny_picture=current_app.config.get('BUNNY_PICTURE', False))

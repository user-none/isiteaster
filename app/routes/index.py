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

from ..utils.easter import easter_date
from ..utils.tz import get_tz

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    tz = get_tz(request, current_app.config)
    today = datetime.now(tz).date()
    easter = easter_date(today.year)

    if easter == today:
        iseaster = True
        easter_is_on = 'Today is Easter!'
    else:
        iseaster = False
        if easter < today:
            easter = easter_date(today.year + 1)
        easter_is_on = 'Easter is on {0:%B} {day}, {year}'.format(easter, day=easter.day, year=easter.year)

    return render_template('index.j2', iseaster=iseaster, easter_is_on=easter_is_on)

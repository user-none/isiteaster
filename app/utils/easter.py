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

from datetime import datetime, date

from .tz import get_tz

def easter_date(year: int) -> date:
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    g = ((8 * b) + 13) // 25
    h = ((19 * a) + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + (2 * e) + (2 * i) - h - k) % 7
    m = ((a + (11 * h)) + (19 * i)) // 433
    n = (h + l - (7 * m) + 90) // 25 # month
    p = (h + l - (7 * m) + (33 * n) + 19) % 32 # day

    return date(year, n, p)

def when_is_easter(request, config) -> (bool, date):
    today = datetime.now().date()
    today_m2 = date(today.year, today.month, today.day - 2)
    today_p2 = date(today.year, today.month, today.day + 2)
    easter = easter_date(today.year)

    # Within 2 days we need to do some lookups to take into account timezone
    # of the visitor
    if easter > today_m2 and easter < today_p2:
        tz = get_tz(request, config)
        today = datetime.now(tz).date()

    if easter == today:
        return True, None
    elif easter < today:
        # Easter already happened, we need to look to next year
        easter = easter_date(today.year + 1)

    return False, easter

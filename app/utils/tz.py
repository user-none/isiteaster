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

import json

from datetime import datetime, timezone
from ipaddress import ip_address

from crawlerdetect import CrawlerDetect

from .. import cache

def _ip_tz_offset_cache_key(ip):
    return '{ip}_tz_offset'.format(ip=ip)

def _is_private_ip(ip):
    return ip_address(ip).is_private

def _get_ip_tz_delta(ip):
    delta = None

    try:
        j = None
        url = 'https://api.ipgeolocation.io/timezone?ip={ip}&apiKey={key}'.format(ip=ip, key=config.get('IPGEO_API_KEY'))
        with urllib.request.urlopen(url, timeout=2) as f:
            j = json.loads(f.read().decode('utf-8'))

        if not j:
            raise Exception('Empty JSON')

        offset = j.get('timezone_offset', None)
        if offset == None:
            raise Exception('Missing timezone offset')

        delta = timedelta(hours=offset)
    except:
        pass

    return delta

def get_tz(request, config):
    # Don't try to determine timezone if not configured to look up timezone by
    # IP address geo location
    if not config.get('IPGEO_API_KEY'):
        return None

    # Don't try to get lookup internal IP 
    if config.get('REQUESTS_PROXIED'):
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    else:
        ip = request.remote_addr
    if not ip or _is_private_ip(ip):
        return None

    # Don't try to waste lookups on crawlers
    user_agent = request.headers.get('User-Agent')
    crawler_detect = CrawlerDetect(user_agent=user_agent)
    if not user_agent or crawler_detect.isCrawler():
        return None

    # Try pulling the tz offset for the ip from the cache
    offset = cache.get(_ip_tz_offset_cache_key(ip))
    if offset:
        delta = timedelta(seconds=offset)
        return timezone(delta)

    # Get timezone offset from geo IP service
    delta = _get_ip_tz_delta(ip)

    # Use system timezone if we can't get the IP's for some reason
    if not delta:
        delta = datetime.now(timezone.utc).astimezone().utcoffset()

    # Cache offset
    cache.set(_ip_tz_offset_cache_key(ip), delta.utcoffset().total_seconds())

    return timezone(delta)

# Copyright (C) 2013 Fox Wilson, Peter Foley, Srijay Kasturi, Samuel Damashek, James Forcier and Reed Koser
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import json
import re
from urllib.request import urlopen, Request
from helpers.hook import Hook


#FIXME: duplicated in commands/reddit.py
def check_exists(subreddit):
    req = Request('http://reddit.com/subreddits/search.json?q=%s' % subreddit, headers={'User-Agent': 'CslBot/1.0'})
    data = json.loads(urlopen(req).read().decode())
    return len(data['data']['children']) > 0


@Hook(types=['pubmsg', 'action'], args=[])
def handle(send, msg, args):
    match = re.search(r'(?:^|\s)/r/([\w|^/]*)\b', msg)
    if not match:
        return
    subreddit = match.group(1)
    if not check_exists(subreddit):
        return
    req = Request('http://reddit.com/r/%s/about.json' % subreddit, headers={'User-Agent': 'CslBot/1.0'})
    data = urlopen(req).read().decode()
    data = json.loads(data)['data']
    for line in data['public_description'].splitlines():
        send(line)
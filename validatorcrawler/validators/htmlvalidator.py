# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import re
import tidy
from BeautifulSoup import BeautifulSoup

class HTMLValidator(object):
    mimetype = 'text/html'

    def __init__(self, content):
        self.content = content

    def validate(self):
        return tidy.parseString(self.content).errors

    def urls(self):
        soup = BeautifulSoup(self.content)
        urls = []

        for tag in soup.findAll(re.compile(r'a|link')):
            try:
                urls.append(tag['href'])
            except KeyError:
                pass

        for tag in soup.findAll(re.compile(r'img|script')):
            try:
                urls.append(tag['src'])
            except KeyError:
                pass

        return urls

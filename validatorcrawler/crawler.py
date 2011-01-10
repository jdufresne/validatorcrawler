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


import urllib2
import urlparse
from validatorcrawler.validators.htmlvalidator import HTMLValidator
import logging

class Crawler(object):
    def __init__(self, start, timeout):
        result = urllib2.urlopen(start)
        self.start = result.url
        self.domain = urlparse.urlparse(result.url).netloc
        self.timeout = timeout
        self.validators = {}
        self.add_validator(HTMLValidator)
        self.logger = logging.getLogger(self.__class__.__name__)

    def add_validator(self, validator):
        self.validators[validator.mimetype] = validator

    def crawl(self):
        visited = set()
        urls = [self.start]
        while urls:
            url = urls.pop(0)
            if url not in visited:
                visited.add(url)
                urls.extend(self.visit(url))
        self.logger.info("Processed %(count)s urls", {'count': len(visited)})

    def visit(self, url):
        try:
            result = urllib2.urlopen(url, timeout=self.timeout)
        except urllib2.HTTPError as error:
            self.logger.error("%(method)s %(url)s %(status)s %(message)s", {
                'method': 'GET',
                'url': error.url,
                'status': error.code,
                'message': error.msg,
            })
        except urllib2.URLError as error:
            self.logger.error("%(method)s %(url)s %(error)s", {
                'method': 'GET',
                'url': url,
                'error': error.reason,
            })
        else:
            self.logger.info("%(method)s %(url)s %(status)s %(message)s", {
                'method': 'GET',
                'url': result.url,
                'status': result.code,
                'message': result.msg,
            })
            if urlparse.urlparse(result.url).netloc == self.domain:
                mimetype = result.info().gettype()
                try:
                    validator = self.validators[mimetype](result.read())
                except KeyError:
                    pass
                else:
                    errors = validator.validate()
                    if errors:
                        for error in errors:
                            if error.severity == 'W':
                                logger = self.logger.warning
                            elif error.severity == 'E':
                                logger = self.logger.error
                            else:
                                logger = self.logger.debug
                            logger('%s', error)

                    return [urlparse.urljoin(url, next_url)
                            for next_url in validator.urls()]
        return []

import urllib2
import urlparse
from validatorcrawler.validators.htmlvalidator import HTMLValidator

import logging


class Crawler(object):
    def __init__(self, start, timeout):
        f = urllib2.urlopen(start)
        self.start = f.url
        self.domain = urlparse.urlparse(f.url).netloc
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
            f = urllib2.urlopen(url, timeout=self.timeout)
        except urllib2.HTTPError as e:
            self.logger.error("%(method)s %(url)s %(status)s %(message)s", {
                'method': 'GET',
                'url': e.url,
                'status': e.code,
                'message': e.msg,
            })
        except urllib2.URLError as e:
            self.logger.error("%(method)s %(url)s %(error)s", {
                'method': 'GET',
                'url': url,
                'error': e.reason,
            })
        else:
            self.logger.info("%(method)s %(url)s %(status)s %(message)s", {
                'method': 'GET',
                'url': f.url,
                'status': f.code,
                'message': f.msg,
            })
            if urlparse.urlparse(f.url).netloc == self.domain:
                mimetype = f.info().gettype()
                try:
                    validator = self.validators[mimetype](f.read())
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

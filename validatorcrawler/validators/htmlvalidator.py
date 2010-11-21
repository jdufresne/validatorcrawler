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

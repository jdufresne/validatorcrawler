# This file is part of validatorcrawler <http://github.com/jdufresne/validatorcrawler>.
#
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


import argparse
import logging
from validatorcrawler.crawler import Crawler

def main():
    VERBOSITY = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('--timeout', '-t', type=int, default=5)
    parser.add_argument(
        '--verbosity', '-v',
        default='info',
        choices=VERBOSITY.keys()
    )
    parser.add_argument('urls', metavar='URL', nargs='+')
    args = parser.parse_args()

    logging.basicConfig(level=VERBOSITY[args.verbosity])
    for url in args.urls:
        crawler = Crawler(url, args.timeout).crawl()

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

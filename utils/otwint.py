import argparse
import subprocess
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
#from multiprocessing.pool import MaybeEncodingError # TODO: handle ending exception
from datetime import datetime
from datetime import timedelta
import time

dtformat = "%Y-%m-%d"

#ARGS: id, search, since, until, es, it
def create_process(args):
    request = 'twint -s \"{}\" --since {} --until {} -es {} -it {} --count'.format(
        args['search'], args['since'], args['until'], args['elasticsearch'], args['index_tweets'])
    print("create_process |{}|\n{}".format(args['id'], request))
    p = subprocess.Popen(request, shell=True)
    p.wait()
    print("finished process |{}|".format(args['id']))
    return p
        
def main(args):
    print("run")
    since = datetime.strptime(args.since, dtformat).date()
    until = datetime.strptime(args.until, dtformat).date()

    # Prepaire arguments array.
    end = since + timedelta(days=args.request_days)
    arguments = [{
        'search': args.search,
        'since': since.strftime(dtformat),
        'until': end.strftime(dtformat),
        'elasticsearch': args.elasticsearch,
        'index_tweets': args.index_tweets,
        'id': 0}]
    i = 1
    while end < until:
        since = since + timedelta(days=args.request_days)
        end = since + timedelta(days=args.request_days)
        if end > until:
            end = until
        arguments.append({
        'search': args.search,
        'since': since.strftime(dtformat),
        'until': end.strftime(dtformat),
        'elasticsearch': args.elasticsearch,
        'index_tweets': args.index_tweets,
        'id': i})
        i += 1
    print("Ranges to fetch {}".format(len(arguments)))

    print('--Start fetching--')
    pool = Pool( processes=args.maximum_instances)
    pool.map(create_process, arguments)
    print('--Fetching ended--')

def options():
    """ Parse arguments
    """
    ap = argparse.ArgumentParser(prog="otwint",
                                 usage="python3 %(prog)s [options]",
                                 description="OTWINT - An Advanced [OPTIMIZED] Twitter Scraping Tool.")
    ap.add_argument("-s", "--search", help="Search for Tweets containing this word or phrase.")
    ap.add_argument("-es", "--elasticsearch", help="Index to Elasticsearch.")
    ap.add_argument("-t", "--timedelta", help="Time interval for every request.")
    ap.add_argument("-rd", "--request-days", help="Days to search in one instance.", default="1")
    ap.add_argument("-mi", "--maximum-instances", help="Maximum instances at time.",  default="8")
    ap.add_argument("--since", help="Filter Tweets sent since date (Example: 2017-12-27).")
    ap.add_argument("--until", help="Filter Tweets sent until date (Example: 2017-12-27).")
    ap.add_argument("--count", help="Display number of Tweets scraped at the end of session.", action="store_true")
    ap.add_argument("-it", "--index-tweets", help="Custom Elasticsearch Index name for Tweets.", nargs="?", default="twinttweets")
    args = ap.parse_args()
    args.request_days = int(args.request_days)
    args.maximum_instances = int(args.maximum_instances)
    return args

if __name__ == '__main__':
    args = options()
    main(args)

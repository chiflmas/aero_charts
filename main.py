#!/usr/bin/env python3
import aip_functions as aip
from airports import airports
import requests
from bs4 import BeautifulSoup
import itertools
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def main():
    # URL
    url = 'https://aip.enaire.es/AIP/'
    # Request
    r = requests.get(url=url)
    # Soup
    soup = BeautifulSoup(r.content, "html.parser")
    # Create folders
    aip.create_airport_folders(airports, 0o755, soup)
    # Create list of urls to request
    urls = list(map(aip.create_url,
                    itertools.repeat(url, len(aip.parse_pdf(soup))),
                    aip.parse_pdf(soup)))
    threads = []
    # Counters
    downloads = 0
    exceptions = 0
    # Time counter init
    t1 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=20) as executor:
        for url in urls:
            file = aip.file_name(url)
            threads.append(executor.submit(aip.download_file,
                                           url,
                                           aip.create_path(soup),
                                           file))
    # Counter of task completed and exceptions
    for task in as_completed(threads):
        if task.done():
            downloads += 1
        if task.exception():
            exceptions += 1
    # Time counter end
    t2 = time.perf_counter()
    # Wait until tqdm last bar finishes
    time.sleep(10)
    # Print results
    print('\n{} flying charts downloaded in {} seconds with {} exceptions.'.format(downloads,
                                                                                  round((t2-t1),0),
                                                                                  exceptions))


if __name__ == '__main__':
    main()

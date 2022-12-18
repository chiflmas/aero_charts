#!/usr/bin/env python3
import aip_functions as aip
import requests
from bs4 import BeautifulSoup
import itertools
from concurrent.futures import ThreadPoolExecutor

# OACI airport list
airports = ['LECH', 'LERI', 'LEPP', 'LEMH', 'LELL', 'LEIB',
            'LEPA_LESJ', 'LELC', 'LEGE', 'LEAL', 'LESB', 'LEPO',
            'LERS', 'LXGB', 'LEAM', 'LEZG', 'LEMD', 'LEBB', 'LEXJ', 'LEBA',
            'LEVX', 'LEZL', 'LEBG', 'LESA', 'LETO', 'LELN', 'LEAS', 'LEVD',
            'LEGT', 'LERJ', 'LESO', 'LEVT', 'LECO', 'LEST', 'LEMO', 'LEGA',
            'LEDA', 'LESU', 'LEJR', 'LEMI', 'LETL', 'GCLP', 'GCLA', 'GCXO',
            'GCRR', 'GSVO', 'GSAI', 'GCTS', 'GCFV', 'GCHI', 'GEML', 'LEMG',
            'LEGR', 'LEHC', 'LEBZ', 'LEBL', 'LEAB', 'LECU_LEVS', 'GCGM', 'LEVC',
            'LERT', 'LERL', 'LEAG', 'LEAO', 'GEHM', 'GECE', 'LECV', 'LEEC',
            'LETA', 'LELO', 'GCXM', 'LEBT']


def main():
    # URL
    url = 'https://aip.enaire.es/AIP/'
    # Request
    r = requests.get(url=url)
    # Soup
    soup = BeautifulSoup(r.content, "html.parser")
    aip.create_airport_folders(airports, 0o755, soup)
    urls = list(map(aip.create_url,
                    itertools.repeat(url, len(aip.parse_pdf(soup))),
                    aip.parse_pdf(soup)))
    threads = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for url in urls:
            file = aip.file_name(url)
            threads.append(executor.submit(aip.download_file,
                                           url,
                                           aip.create_path(soup),
                                           file))


if __name__ == '__main__':
    main()

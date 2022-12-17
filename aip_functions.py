#!/usr/bin/env python3
import os
import re
from concurrent.futures import ThreadPoolExecutor

import requests
from tqdm import tqdm

def file_name(url):
    """
    Split a URL by /
    :param url: URL
    :return: Group of strings after last /
    """
    file_name = url.split("/")[-1]
    return file_name

def create_url(url, pdf):
    """
    Joins base urls and pdf name to create the pdf url
    :param url: URL
    :param pdf: file_name
    :return: URL + PDF
    """
    url = url + pdf
    return url

def parse_pdf(soup):
    """
    Extract AD2 and AD3 PDF names from html request
    :param soup: bs4 request from aip.enaire.es
    :return: List of pdf names
    """
    pdf = []
    for a in soup.find_all('a', href=True):
        pdf.append(a['href'])
    pdf = list(filter(lambda i: ("AD2" or "AD3") in i,
                      filter(lambda i: "pdf" in i, pdf)))
    return pdf

def create_path(soup):
    """
    Creates path with date+airac date format
    :param soup: bs4 request from aip.enaire.es
    :return: string with path
    """
    from datetime import date
    today = date.today()
    date = today.strftime("%d_%m_%Y")
    airac_cycle = soup.find('div', {'class': 'actualizado'}).get_text(strip=True)
    path = ''.join((date, '(', re.findall(r'(^[^\s]+)', airac_cycle)[0], ')'))
    return path

def create_airport_folders(airports, access_rights, soup):
    """
    Creates the folder structure where the flying charts will be saved
    :param airports: list with the OACI airport codes
    :param access_rights: access rights code
    :param soup: bs4 request from aip.enaire.es
    :return: 2 level folder structure
    """
    path = create_path(soup)
    try:
        os.mkdir(path, access_rights)
    except OSError:
        print("\nCreation of the directory %s failed" % path)
    else:
        print("\nSuccessfully created the directory %s" % path)
    for airport in airports:
        try:
            os.mkdir(path + "/" + airport, access_rights)
        except OSError:
            print("\nCreation of the directory %s failed" % (path + "/" + airport))
        else:
            print("\nSuccessfully created the directory %s" % (path + "/" + airport))

def download_file(url, path, file_name):
    """
    Download PDF air chart from URL and saves it in the OACI airport folder
    :param url: pdf URL
    :param path: Parent folder path
    :param file_name: pdf name
    :return: pdf file
    """
    try:
        # Request
        html = requests.get(url, stream=True) # Stream to get data in chunks for tqdm
        if html.status_code != 200:
            print('\nFailure Message {}'.format(html.text))
        #OACI code folder
        folder = re.findall(r'.*\/(.*)\/.*', url)[0]
        # Save pdf to oaci airport folder
        with open(path + "/" + folder + "/" + file_name, 'wb+') as f:
            # Progress bar init
            pbar = tqdm(unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                        #leave=False,
                        total=int(html.headers['Content-Length']))
            pbar.clear()
            # Pbar description
            pbar.set_description("Downloading {}".format(file_name))
            for chunk in html.iter_content(chunk_size=1024):
                if chunk:
                    pbar.update(len(chunk))
                    f.write(chunk)
            pbar.close()
    except requests.exceptions.RequestException as e:
        print(e)

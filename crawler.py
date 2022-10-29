""" crawler.py: Quick script to scrape PDF papers from Google Scholar of the SIGCHI Conference.

Examples:
    $ python3 crawler.py --help
    $ python3 crawler.py --from-file doi_authors.json
    $ python3 crawler.py --from-file doi_authors.json --slow
    $ python3 crawler.py --from-file doi_authors.json --bib-output references.bib
Requires:
    Packages 'scholarly' and 'BeautifulSoup' from pip3.
"""

from sys import stderr
from sys import exit
import argparse
import string
#from turtle import title
import requests
import random
from functools import partial
import time
import sys
import os
import json

from scholarly import scholarly
from scholarly import ProxyGenerator

#from scholarly import _get_page

printerr = partial(print, file=stderr, flush=True)



class PdfTooSmallError(Exception):
    """ Raise if downloaded pdf is too small."""
    pass


""" In case of String matching or the PDF Title of the SIGCHI is wrong"""


#def fuzzy_1_in_2(str1, str2):
#    """ Fuzzy match if str1 is a sub-string of str2."""
#    def cleanup(text):
#        ascii_only = filter(lambda i: i in string.ascii_letters, text)
#        return ''.join(list(ascii_only)).lower()
#    return cleanup(str1) in cleanup(str2)



def download_pdf(pdf_url, title, count):
    """ Download and save paper as {title}.pdf."""

    # Handle occasional strange format:
    if pdf_url[0:26] == 'https://scholar.google.com':
        pdf_url = pdf_url[26:]

    # Download and check length.

    try:
        pdf = requests.get(pdf_url, allow_redirects=True)

    except requests.exceptions.InvalidSchema as e:
        list_pdf_not_downloaded.append(count)
        print("Error in {} index number of {}".format(title, count))
        printerr("ERROR\t\t INVALID PDF URL: " + pdf_url)
        pdf = None

    if pdf:
        if len(pdf.content) < 10000:
            raise PdfTooSmallError
        # Write to file.
        with open(str(count) + ".pdf", 'wb') as f:
            f.write(pdf.content)


def get_first_paper_info(search_str, count):
    """ Get paper information from Google Scholar."""
    print("Searching for: ", search_str)
    search = scholarly.search_pubs(search_str)
    first_paper = next(search)
    title = first_paper['bib']['title']

    time.sleep(random.uniform(2, 4))
    # bibtex = _get_page(first_paper.url_scholarbib)

    #if not fuzzy_1_in_2(title, search_str):
    #    printerr("%% ERROR\t\t TITLE NOT IN SEARCH - MAY BE WRONG PAPER")

    try:
        pdf_url = first_paper['eprint_url']
    except KeyError:
        list_pdf_not_downloaded.append(count)
        printerr("ERROR\t\t PDF URL NOT FOUND: " + title)
        pdf_url = None

    #return title, bibtex, pdf_url

    return title, pdf_url


def retrive_paper(search_str, count ,bibtex_file=None):
    """ Save paper, print bibtex (to file if provided)."""

    # Try to download from scholar.
    try:
        #title, bibtex, pdf_url = get_first_paper_info(search_str, count)
        title, pdf_url = get_first_paper_info(search_str, count)

    except StopIteration:
        list_pdf_not_downloaded.append(count)
        print("Error in {} index number of {}".format(search_str, count))
        printerr("ERROR: COULD NOT ACCESS. CAPTCHA or Paper link does not exist.")
        exit(1)

    # Save to bibtex file and print.
    #print(bibtex)
    #if bibtex_file:
    #    with open(bibtex_file, "a") as f:
    #        f.write(bibtex)

    # Try to download PDF.
    try:
        if pdf_url:
            download_pdf(pdf_url, title, count)
    except requests.exceptions.ConnectionError:
        list_pdf_not_downloaded.append(count)
        print("Error in {} index number of {}".format(search_str, count))
        printerr("ERROR\t\t INVALID PDF URL: " + pdf_url)
    except PdfTooSmallError:
        list_pdf_not_downloaded.append(count)
        print("Error in {} index number of {}".format(search_str, count))
        printerr("ERROR\t\t PDF MAY BE TOO SMALL: " + title)
    print("")



def main(args):

    #if args.search:
    #    retrive_paper(args.search, args.bib_output) #Debug only

    if args.from_file:
        try:
            with open("doi_authors.json", 'r') as f:
                titles = json.load(f)

            for i in range(0, 5): #Missing 6.pdf and 98.pdf #6483
                print("Title: ", titles[i]['Title'])
                
                search = titles[i]['Title']
                
                retrive_paper(search,  i + 1, args.bib_output)
                if args.slow:
                    wait = random.uniform(60, 75)
                    print(f"Waiting {wait:5.0f} seconds")
                    time.sleep(wait)        


        except FileNotFoundError:
            printerr("ERROR:\t\t Json file not found.")
    else:
        parser.print_help()



if __name__ == "__main__":
    #group.add_argument("--search", type=str,
    parser = argparse.ArgumentParser(description="Papers from Google Scholar.")
    group = parser.add_mutually_exclusive_group()
    #                    help="Enter a single paper search query.") #Debug only
    group.add_argument("--from-file", type=str,
                        help="Read search strings, one per line from a JSON file.")
    parser.add_argument("--bib-output", type=str,
                        help="Append the BibTex output to a file.")
    parser.add_argument("--slow", action="store_true", default=False,
                        help="Go much slower in an attempt to avoid CAPTCHAs.")
    args = parser.parse_args()

    list_pdf_not_downloaded = []

    # Set up a ProxyGenerator object to use free proxies
    # This needs to be done only once per session
    
    pg = ProxyGenerator()
    success = pg.FreeProxies()
    #success = pg.Tor_Internal(tor_cmd = "tor")
    scholarly.use_proxy(pg)

    print("Proxy done\n")

    #python ../crawler.py --from-file ../doi_authors.json --slow

    main(args)

    print(list_pdf_not_downloaded)
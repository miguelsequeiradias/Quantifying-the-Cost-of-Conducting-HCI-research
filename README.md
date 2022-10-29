Quantifying the Cost of conducting HCI research
====================
## Introduction

This project was developed in the aim of Quantifying the Cost of conducting HCI research, my Thesis, and for this we needed the Full-Text PDF files from the proceedings of the CHI Conference.

This project downloads all full-text PDF's from the DBLP open-access library as well as the DOI, the Authors, the Full Title and the Number of Citations.

Cheers,<br>
Miguel

<br>

##  - Pre-Requisites

- Scholarly
```bash
pip install scholarly
```
- Beautiful Soup
```bash
pip install beautifulsoup4
```
- Semantic Scholar
```bash
pip install semanticscholar
```

<br>

## Optional dependencies
- TOR
```bash
pip install scholarly[tor]
```
<br>

## How to use

```bash
cd Papers/
python3 ../scraper.py
python3 ../crawler.py --from-file ../doi_authors.json --slow
python3 search_keywords.py
cd ../
python3 doi_citations.py
```

<br>

## File structure

```
📦Quantifying-the-Cost-of-conducting-HCI-research
 ┣ 📂Papers
 ┃ ┗ 📜search_keywords.py
 ┣ 📜.gitignore
 ┣ 📜README.md
 ┣ 📜crawler.py
 ┣ 📜dataset.csv
 ┣ 📜doi_citations.py
 ┗ 📜scraper.py
```

<br>

## Warnings
Both google scholars and ACM digital Library will block IP after sending so many requests. In my experience, I got blocked from ACM after a 500-1000 request. Therefore, I had to run the Crawler with a small range of papers to download.
I put a sleep code to control each loop run time. However, this problem will continue. I would suggest using multiple computers or using a TOR proxy which is commented in the Crawler.

<br>

## Contributions
We welcome contributions from you. Please create an issue, fork this repository and submit a pull request. 
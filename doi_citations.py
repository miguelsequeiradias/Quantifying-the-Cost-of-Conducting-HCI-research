from semanticscholar import SemanticScholar
import json
import csv
import re
import random
import time


outfile = open('doi_citations.csv','a', newline='')
writer = csv.writer(outfile)
writer.writerow(["Paper Index", "DOI", "Citation"])
sch = SemanticScholar()

with open("doi_authors.json", 'r') as f:
    json_decoded = json.load(f)

counter = 0

for i in range(0, 9688):

    doi_link = json_decoded[i]['doi']
    p_id = json_decoded[i]['doi']

    l = re.compile("(10\.[^/]+/([^(\s\>\"\<})])+)").split(doi_link)
    paper = sch.get_paper(l[1])
    writer.writerow([i + 1, doi_link, paper.citationCount])
    print(str(i+1) + " ----------> " + doi_link + "--------> " + str(paper.citationCount))
    counter = counter + 1

    if counter == 100:
        print(f"Waiting {350:5.0f} seconds")
        time.sleep(300)
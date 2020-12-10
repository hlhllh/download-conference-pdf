# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 19:17:10 2020

@author: hexu0003
"""
import re
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import requests
import os
from tqdm import tqdm

def check(keywords, file_name):
    file_name = file_name.lower()
    if len(keywords) == 0:
        return True  # download all papers
    
    for key in keywords:
        if key in file_name:
            return True
    return False

rl_key_words = ['reinforce', 'reinforcement', 'policy', 'markov', 'actor', 'q-value', 'critic', 'multi-agent']
    
#Grab all the links in this directory
URL="https://proceedings.neurips.cc/paper/2020"

http = httplib2.Http()
status, response = http.request(URL)

papers=[]

#will go through the URL, and output list "papers" of the PDF links
for link in BeautifulSoup(response,"html.parser", parse_only=SoupStrainer('a')):
    if link.has_attr('href'):
        #print(link['href'])
        identifier=link['href']
        identifier=identifier.replace("Abstract.html", "Paper.pdf")
        identifier=identifier.replace("hash", "file")
        full_url="https://proceedings.neurips.cc"+identifier
        papers.append(full_url)

#delete first 3 entries in the papers, and last one because they are not good.
del papers[:3]
del papers[-1]

subdirectory="pdfs"
path = r'D:\NIPS20'

for i in tqdm(range(len(papers))):
    link = papers[i]
# for link in papers:
    r = requests.get(link, allow_redirects=True)
    d = r.headers['content-disposition']
    fname = re.findall("filename=(.+)", d)[0]
    # name = link.rsplit('/',1)[1]
    if check(rl_key_words, fname):
        full_path = os.path.join(path, fname)
        open(full_path, 'wb').write(r.content)
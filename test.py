#lyrics generator with python

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import pandas as pd

total_links = [ 'http://ohhla.com/all.html',
                'http://ohhla.com/all_two.html',
                'http://ohhla.com/all_three.html',
                'http://ohhla.com/all_four.html',
                'http://ohhla.com/all_five.html' ]

def get_links(links):
    soup = BeautifulSoup(requests.get(links).text,'html.parser')
    gross_links = [link['href'] for link in soup.find_all('a',href=True)]
    return gross_links

start=time()

#adding all links together
links_per_total_links = []

processes = []

with ThreadPoolExecutor(max_workers=10) as executor:
    for link in total_links:
        processes.append(executor.submit(get_links,link))

for process in as_completed(processes):
    links_per_total_links.append(process.result())

end=time()

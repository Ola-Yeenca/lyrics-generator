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



#adding all links together
links_per_total_links = []

processes = []

with ThreadPoolExecutor(max_workers=10) as executor:
    for link in total_links:
        processes.append(executor.submit(get_links,link))

for process in as_completed(processes):
    links_per_total_links.append(process.result())





#removing all the links that are not lyrics
all_links =[ item for sublist in links_per_total_links for item in sublist]
unique_links =[]
unique_links = [link for link in all_links if link is not unique_links ]
link_df = pd.DataFrame(unique_links)

#cleaning up the links and getting indexes for each criteria

ohhla = link_df[link_df[0].apply(lambda x: x[:len('http://ohhla.com/')] == 'http://ohhla.com/'.index.tolist())]

amazon = link_df[link_df[0].apply(lambda x: 'http://www.amazon.com/' in x)].index.to_list()

itunes = link_df[link_df[0].apply(lambda x: x[:len('http://itunes.apple.com/')] == 'http://itunes.apple.com/'.index.tolist())]

youtube_music = link_df[link_df[0].apply(lambda x: x[:len('https://music.youtube.com/')] == 'https://music.youtube.com/'.index.tolist())]

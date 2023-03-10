#lyrics generator with python

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from bs4 import BeautifulSoup
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

ohhla = link_df[link_df[0].apply(lambda x: x[:len('http://ohhla.com/')] == 'http://ohhla.com/')].index.tolist()

amazon = link_df[link_df[0].apply(lambda x: 'http://www.amazon.com/' in x)].index.tolist()

itunes = link_df[link_df[0].apply(lambda x: x[:len('http://itunes.apple.com/')] == 'http://itunes.apple.com/')].index.tolist()

youtube_music = link_df[link_df[0].apply(lambda x: x[:len('https://music.youtube.com/')] == 'https://music.youtube.com/')].index.tolist()

apk = link_df[link_df[0].apply(lambda x: x[:len('https://www.apkfollow.com/')] == 'https://www.apkfollow.com/')].index.tolist()

all_text = link_df[link_df[0].apply(lambda x: x[:len('all')]=='all')].index.tolist()

all_html = link_df[link_df[0].apply(lambda x:'.html' in x )].index.tolist()

rap_reviews = link_df[link_df[0].apply(lambda x: x[:len('https://www.rapreviews.com/')] == 'https://www.rapreviews.com/')].index.tolist()


#removing all the links that are not lyrics

total_remove = ohhla + amazon + itunes + youtube_music + apk + all_html + rap_reviews
link_df.drop(total_remove,inplace=True)
link_df.to_csv('initial_directories.txt',header=False,index=False)

#getting sub directories of artistes

start = time()

dir_list = pd.read_csv(r'initial_directories.txt',header=None)[0].tolist()
sub_dir_list = []

def get_sub_links(links):
    url = 'http://ohhla.com/' + links
    soup = BeautifulSoup(requests.get(url).text,'html.parser')
    gross_links = [links + link['href'] for link in soup.find_all('a',href=True) if '/' in link ['href'] and 'anonymous' not in link['href']]

    return gross_links

processes = []

with ThreadPoolExecutor(max_workers=10) as executor:
    for link in dir_list:
        processes.append(executor.submit(get_sub_links,link))

for process in as_completed(processes):
    sub_dir_list.append(process.result())


unpacked_sub_dir_list = [item for each_dir in sub_dir_list for item in each_dir]

sub_dir_df = pd.DataFrame(unpacked_sub_dir_list).to_csv('total_sub_directories.txt',header=False,index=False)

#get links for all text files

start = time()

all_dir_link = pd.read_csv(r'total_sub_directories.txt',header=None)[0].tolist()

text_links = []

def get_text_links(links):
    url = 'http://ohhla.com/' + links
    soup = BeautifulSoup(requests.get(url).text,'html.parser')
    gross_links = [links + link['href'] for link in soup.find_all('a',href=True) if '.txt' in link['href']]
    return gross_links

processes = []

with ThreadPoolExecutor(max_workers=10) as executor:
    for link in all_dir_link:
        processes.append(executor.submit(get_links,link))

for process in as_completed(processes):
    links_per_total_links.append(process.result())

unpacked_text_links = [item for each_dir in text_links for item in each_dir]

end = time()

print(end-start)

pd.DataFrame(unpacked_text_links).to_csv('total_text_links.txt',header=False,index=False)

#scraping lyrics

start = time()

all_text_links = pd.read_csv(r'total_text_links.txt',header=None)[0].tolist()


def get_lyrics(text_links):
    url = 'http://ohhla.com/' + text_links
    html =requests.get(url).text
    soup = BeautifulSoup(html,'html.parser')
    time.sleep(1)


    if soup.find('pre'):
        double_loc = soup.find('pre').text.find("|n|n") + 2
        return soup.find('pre').text[double_loc:]
    else:
        double_loc = html.find('n|n') + 2
        return html[double_loc:]


lyrics = []

processes = []

with ThreadPoolExecutor(max_workers=10) as executor:
    for count, link in enumerate(text_links['Text_Link']):
        print(count)
        processes.append(executor.submit(get_lyrics,link))

for process in as_completed(processes):
    links_per_total_links.append(process.result())
    [[]]

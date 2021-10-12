import requests
from bs4 import BeautifulSoup
import pprint

response = requests.get("https://news.ycombinator.com/")
res2 = requests.get("https://news.ycombinator.com/news?p=2")
soup = BeautifulSoup(response.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

count = 0
for link in soup.find_all('a'):
    print(link)
    count += 1

print(f"Esse site tem um total de {count} links")

# use css selectors em web scrapping
print(soup.select('.score'))  # classe
print(soup.select('#score_28830921'))  # id

print(soup.select('.storylink')[0])
links = soup.select('.storylink')
subtext = soup.select('.subtext')
links2 = soup2.select('.storylink')
subtext2 = soup2.select('.subtext')

mega_links = links2 + links
mega_subtext = subtext2 + subtext


def sort_stories_by_vote(hnlist):
    return sorted(hnlist, key= lambda k:k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for index, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[index].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_vote(hn)[:5]


pprint.pprint(create_custom_hn(mega_links, mega_subtext))

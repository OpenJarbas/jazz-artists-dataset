import csv
import string
import sys

import requests
# some important modules to scrape a website.
from bs4 import BeautifulSoup


def scrap_letter(letter):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"}

    page = requests.get(f'http://www.jazzmusicarchives.com/ListArtistsAlpha.aspx?letter={letter}', headers=headers)

    if page.status_code != 200:
        sys.exit('Non 200 status code received')

    soup = BeautifulSoup(page.content, 'html.parser')

    artist = []
    genres = []
    countries = []
    urls = []
    for li in soup.find_all("li"):
        a = li.find("a")
        if not a.get("href", "").startswith("/artist/") or "#shout" in a.get("href", ""):
            continue
        span = li.find("span")
        if " • " not in span.get_text():
            continue
        genre, country = span.get_text().split(" • ")
        genres.append(genre.strip())
        countries.append(country.strip())

        art = a.get_text().strip()
        if "," in art:
            s = art.split(",")
            art = f"{s[1]} {s[0]}".strip()
        artist.append(art)
        url = f"http://www.jazzmusicarchives.com{a['href']}"
        urls.append(url)

    # Save the dataset in csv file.
    colums_names = ['artist', 'genre', 'country', 'url']
    with open(f'./raw_{letter.upper()}_jazz_musicarchives.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(colums_names)
        writer.writerows(list(set(zip(artist, genres, countries, urls))))

    f.close()


for letter in string.ascii_lowercase[:26]:
    scrap_letter(letter)

import urllib.request as rq
from collections import ChainMap

from bs4 import BeautifulSoup
from firebase_admin import db


def get_content_page(url):
    html_content = rq.urlopen(url).read().decode()
    soup = BeautifulSoup(html_content, "html.parser")
    return soup


def get_level(total):
    option = (total % 4)
    options = {
        0: (total / 4),
        1: ((total + 3) / 4),
        2: ((total + 2) / 4),
        3: ((total + 1) / 4)
    }
    level = options.get(option)
    return int(level)


def web_scraping(initial=False):
    base_url = "https://www.eso.org/public/images/potw/list/"
    initial_content = get_content_page(base_url + "1/")
    publications = initial_content.find_all("div", {"class": "news-wrapper"})
    world_ref = db.reference('/worlds')
    worlds_firebase = world_ref.get()
    worlds = {}
    images_keys = []
    if worlds_firebase:
        worlds = dict(worlds_firebase)
        images_keys = list(dict(ChainMap(*worlds.values())).keys())
    count = len(images_keys) + 1
    last_level = get_level(count)
    if initial:
        for i in range(2, 15):
            aux_content = get_content_page(base_url + "{}/".format(i))
            aux_publications = aux_content.find_all("div", {"class": "news-wrapper"})
            publications = publications + aux_publications
    aux_dict = {}
    for pub in publications:
        id = pub.find("div", {"class": "news-id"}).get_text().split(" — ")[0]
        url = pub.find("div", {"class": "news-image"}).find("img").get("src")
        title = pub.find("div", {"class": "news-title"}).get_text()
        teaser = pub.find("div", {"class": "news-teaser"})
        description = teaser.get_text().split(".")[0]
        if id not in images_keys:
            new_level = get_level(count)
            if new_level != last_level:
                worlds.update({
                    'w{}'.format(last_level): aux_dict
                })
                aux_dict = {}
            aux_dict.update({
                id: {"url": url, "title": title, "description": description}
            })
            images_keys.append(id)
            count = count + 1
            last_level = new_level
    world_ref.set(worlds)

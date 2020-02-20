import urllib.request as rq
from bs4 import BeautifulSoup
from firebase_admin import db


def get_content_page(url):
    html_content = rq.urlopen(url).read().decode()
    soup = BeautifulSoup(html_content, "html.parser")
    return soup

def get_level(total):
    option = (total % 3)
    options = {
        0: (total / 3),
        1: ((total + 2) / 3),
        2: ((total + 1) / 3)
    }
    level = options.get(option)
    return level


def web_scraping(initial=False):
    base_url = "https://www.eso.org/public/images/potw/list/"
    initial_content = get_content_page(base_url + "1/")
    publications = initial_content.find_all("div", {"class": "news-wrapper"})
    image_ref = db.reference('/images')
    images = image_ref.get()
    images_keys = []
    if images:
        images = dict(images)
        images_keys = list(images.keys())
    else:
        images = {}
    count = len(images_keys) + 1
    last_level = get_level(count)
    if initial:
        for i in range(2, 6):
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
                images.update(aux_dict)
                aux_dict = {}
            aux_dict.update({
                id: {
                    "url": url, "title": title, "description": description,
                    "level": new_level
                }
            })
            images_keys.append(id)
            count = count + 1
            last_level = new_level
    image_ref.set(images)

import urllib.request as rq

import firebase_admin
from bs4 import BeautifulSoup
from firebase_admin import db

from worlds.models import Image, World

MONTHS = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12",
}


def create_level(images_per_level):
    images = Image.objects.filter(world__isnull=True).values_list("id", flat=True)
    if len(images) == images_per_level:
        world = World.objects.create()
        Image.objects.filter(id__in=images).update(world_id=world.id)


def get_content_page(url):
    html_content = rq.urlopen(url).read().decode()
    soup = BeautifulSoup(html_content, "html.parser")
    return soup


def add_image_to_dict(id, data, total, current_dict):
    option = (total % 3)
    options = {
        0: (total / 3),
        1: ((total + 2) / 3),
        2: ((total + 1) / 3)
    }
    level = options.get(option)
    data.update({'level': level, 'available': False})
    current_dict.update({id: data})
    return current_dict


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
    if initial:
        for i in range(2, 6):
            aux_content = get_content_page(base_url + "{}/".format(i))
            aux_publications = aux_content.find_all("div", {"class": "news-wrapper"})
            publications = publications + aux_publications
    for pub in publications:
        id = pub.find("div", {"class": "news-id"}).get_text().split(" — ")[0]
        url = pub.find("div", {"class": "news-image"}).find("img").get("src")
        title = pub.find("div", {"class": "news-title"}).get_text()
        teaser = pub.find("div", {"class": "news-teaser"})
        description = teaser.get_text().split(".")[0]
        if not id in images_keys:
            images = add_image_to_dict(
                id,
                {"url": url, "title": title, "description": description},
                count,
                images,
            )
            images_keys.append(id)
            count = count + 1
    image_ref.set(images)

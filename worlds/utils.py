import urllib.request as rq

from bs4 import BeautifulSoup

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


def web_scraping(initial=False):
    base_url = "https://www.eso.org/public/announcements/list/"
    initial_content = get_content_page(base_url + "1/")
    publications = initial_content.find_all("div", {"class": "news-wrapper"})
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
        date = teaser.find("strong").get_text()
        description = teaser.get_text().split(".")[0]
        day, month, year = date.split(" ")
        date = "{}-{}-{:02}".format(year, MONTHS[month], int(day))
        img, created = Image.objects.get_or_create(
            id=id, url=url, title=title, description=description,
            publication_date=date
        )
        if created:
            create_level(3)

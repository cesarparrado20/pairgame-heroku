from celery import shared_task

from worlds.utils import web_scraping


@shared_task
def scraping():
    web_scraping()

from celery import shared_task

from worlds.models import World
from worlds.utils import web_scraping


@shared_task
def scraping():
    World.objects.create()

from django.contrib import admin

from worlds.models import World, Image


@admin.register(World)
class WorldAdmin(admin.ModelAdmin):
    list_display = ["id"]
    list_display_links = ["id"]
    search_fields = ["id"]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["title", "world", "publication_date"]
    list_display_links = ["title", "world", "publication_date"]
    search_fields = ["title"]
    list_filter = ["world"]

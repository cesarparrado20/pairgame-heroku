from rest_framework import serializers

from worlds.models import World, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "title", "description", "url", "publication_date"]


class WorldSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = World
        fields = ["id", "images"]

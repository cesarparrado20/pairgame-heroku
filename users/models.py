from django.contrib.auth.models import User
from django.db import models

from worlds.models import World


class Profile(models.Model):
    avatar = models.ImageField(upload_to="avatars")
    xp_points = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"
        db_table = "profiles"

    def __str__(self):
        return "{}'s profile".format(self.user.username)


class ProfileWorld(models.Model):
    score = models.PositiveIntegerField()
    lost = models.BooleanField(default=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    world = models.ForeignKey(World, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "user result in the worlds"
        verbose_name_plural = "user results in the worlds"
        db_table = "profiles_worlds"

    def __str__(self):
        return "Result of {} in the world #{}".format(self.profile.user.username,
                                                      self.world.id)

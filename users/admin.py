from django.contrib import admin

from users.models import Profile, ProfileWorld


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "xp_points"]
    list_display_links = ["user", "xp_points"]
    search_fields = ["user__username"]


@admin.register(ProfileWorld)
class ProfileWorldAdmin(admin.ModelAdmin):
    list_display = ["profile", "world", "lost", "score"]
    list_display_links = ["profile", "world", "lost", "score"]
    search_fields = ["profile__user__username"]
    list_filter = ["profile", "world"]

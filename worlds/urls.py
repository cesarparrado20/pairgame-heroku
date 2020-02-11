from django.urls import path

from worlds.views import WorldListAPIView, ImageListAPIView

app_name = 'worlds'

urlpatterns = [
    path('api/worlds/', WorldListAPIView.as_view(), name='api_worlds'),
    path('api/images/', ImageListAPIView.as_view(), name='api_images')
]

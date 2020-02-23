from django.urls import path

from users.views import RegisterAPIView, LoginAPIView, FirebaseView

app_name = 'users'

urlpatterns = [
    path('api/register/', RegisterAPIView.as_view()),
    path('api/login/', LoginAPIView.as_view()),
    path('', FirebaseView.as_view(), name='scraping_view'),
]

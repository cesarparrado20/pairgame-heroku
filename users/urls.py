from django.urls import path

from users.views import RegisterAPIView, LoginAPIView

app_name = 'users'

urlpatterns = [
    path('api/register/', RegisterAPIView.as_view()),
    path('api/login/', LoginAPIView.as_view()),
]

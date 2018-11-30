from django.urls import include, path
from app_manage_home import views as manage_home

urlpatterns = [
    path('home/', manage_home.home, name='manage_home_home'),
]
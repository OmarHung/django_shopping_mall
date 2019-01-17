from django.urls import include, path
from app_front_home import views as home

urlpatterns = [
    path('', home.index, name='home'),
]
from django.urls import include, path
from app_manage_login import views as manage_login

urlpatterns = [
    path('check_user/', manage_login.check_user, name='manage_login_check_user'),
    path('logout/', manage_login.logout, name='manage_login_logout'),
    path('login/', manage_login.login, name='manage_login_login'),
]
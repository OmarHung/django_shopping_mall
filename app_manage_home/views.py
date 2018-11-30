from django.shortcuts import render
from app_manage_admin_user import user_decorator
# Create your views here.

@user_decorator.login
def home(request):
    return render(request, 'manage/home.html', {})
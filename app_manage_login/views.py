from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from app_manage_admin_user.models import Admin_user

# Create your views here.
def login(request):
    username = request.session.get('admin_username')

    if username :
        return redirect('manage_home_home')

    return render(request, 'manage/login.html', {})

def check_user(request):
    if request.method == "POST":
        status = 'ERROR'

        username = request.POST['username']
        password = request.POST['password']

        try:
            admin_user = Admin_user.objects.get(username=username)
        except ObjectDoesNotExist or MultipleObjectsReturned:
            response = {'status': status, 'msg': '帳號錯誤'}
            return JsonResponse(response)

        user_status = admin_user.status
        if user_status==0 :
            response = {'status': status, 'msg': '此帳號尚未啟用'}
            return JsonResponse(response)

        user_password = admin_user.password
        check = check_password(password, user_password)
        if not check :
            response = {'status': status, 'msg': '密碼錯誤'}
            return JsonResponse(response)

        request.session['admin_username'] = username
        request.session['admin_name'] = admin_user.name
        request.session['admin_uid'] = admin_user.uid
        request.session['admin_premission'] = admin_user.premission

        url = request.COOKIES.get('url', '')

        response = {'status': 'OK', 'url': url}
        res = JsonResponse(response)
        res.delete_cookie('url')
        return res

def logout(request):
    username = request.session.get('admin_username')

    if username:
        del request.session['admin_username']
        del request.session['admin_name']
        del request.session['admin_uid']

    return redirect(login)
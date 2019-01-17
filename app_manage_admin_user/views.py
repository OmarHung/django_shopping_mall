from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import uuid
from django.contrib.auth.hashers import make_password
import json

from .models import Admin_user
from app_system.models import System_operation_record as Sor
from app_manage_admin_user import user_decorator, user_premission

father_title = "後台使用者"
father_url = "manage_admin_user_item_list"

# Create your views here.
def __init__(request):
    if 'all' not in request.session['admin_premission'] and 'system' not in request.session['admin_premission']:
        return redirect('manage_home_home')

@user_decorator.login
def item_list(request):
    users = Admin_user.objects.all()

    search_text = request.GET.get('search_text', '')
    if search_text!='':
        users = Admin_user.objects.filter(name__icontains=search_text, username__contains=search_text)

    page = request.GET.get('page', 1)
    paginator = Paginator(users, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'manage/admin_user/list.html', {
        'title': '後台使用者',
        'users': users,
        'search_text': search_text,
    })

@user_decorator.login
def item_add(request):
    return render(request, 'manage/admin_user/add.html', {
        'father_title': father_title,
        'father_url': father_url,
        'title': ' 新增後台使用者',
    })

@user_decorator.login
def item_insert(request):
    if request.method == "POST":
        status = 'ERROR'

        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        password_check = request.POST['password_check']
        premission = request.POST.getlist('premission')

        str_premission = ''
        for value in premission:
            str_premission = str_premission + value + ','

        #檢查重複
        check = Admin_user.objects.filter(username=username)
        if check.count()>0:
            response = {'status': status, 'msg': '帳號重複'}
            return JsonResponse(response)

        if password!=password_check:
            response = {'status': status, 'msg': '請確認兩次數入的密碼是否一致'}
            return JsonResponse(response)

        if len(password)<6:
            response = {'status': status, 'msg': '密碼長度需超過6個位元'}
            return JsonResponse(response)

        if str_premission=='':
            response = {'status': status, 'msg': '請選擇權限'}
            return JsonResponse(response)


        uid = uuid.uuid1().hex
        password = make_password(password)

        Admin_user.objects.create(name=name, username=username, password=password, premission=str_premission, uid=uid)

        log = "新增後台使用者：" + name
        type = "新增"
        Sor.objects.create(log=log, type=type)

        response = {'status': 'OK'}
        return JsonResponse(response)

@user_decorator.login
def item_edit(request, id=0):
    try:
        user = Admin_user.objects.get(id=id)
    except ObjectDoesNotExist or MultipleObjectsReturned:
        return redirect(item_list)

    return render(request, 'manage/admin_user/edit.html', {
        'father_title': father_title,
        'father_url': father_url,
        'title': ' 編輯後台使用者',
        'user': user,
    })

@user_decorator.login
def item_update(request):
    if request.method == "POST":
        status = 'ERROR'

        uid = request.POST['uid']
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        password_check = request.POST['password_check']
        premission = request.POST.getlist('premission')

        str_premission = ''
        for value in premission:
            str_premission = str_premission + value + ','

        print(premission)

        #檢查重複
        check = Admin_user.objects.filter(username=username).exclude(uid=uid)
        if check.count()>0:
            response = {'status': status, 'msg': '帳號重複'}
            return JsonResponse(response)

        if len(password)>0:
            if password!=password_check:
                response = {'status': status, 'msg': '請確認兩次數入的密碼是否一致'}
                return JsonResponse(response)

            if len(password)<6:
                response = {'status': status, 'msg': '密碼長度需超過6個位元'}
                return JsonResponse(response)

        if str_premission == '':
            response = {'status': status, 'msg': '請選擇權限'}
            return JsonResponse(response)

        user = Admin_user.objects.filter(uid=uid)
        user.update(name=name, username=username, premission=str_premission)

        if len(password) > 0:
            password = make_password(password)
            user.update(password=password)

        log = "編輯後台使用者：" + name
        type = "編輯"
        Sor.objects.create(log=log, type=type)

        response = {'status': 'OK'}
        return JsonResponse(response)

@user_decorator.login
def item_delete(request, id=0):
    try:
        user = Admin_user.objects.get(id=id)
    except ObjectDoesNotExist or MultipleObjectsReturned:
        return redirect(item_list)
    name = user.name

    user.delete()

    log = "刪除後台使用者：" + name
    type = "刪除"
    Sor.objects.create(log=log, type=type)
    return redirect(item_list)

@user_decorator.login
def update_status(request):
    id      = request.POST['id']
    status  = request.POST['status']

    user = Admin_user.objects.filter(id=id)
    name = user[0].name
    if status=='1':
        status = 0
        log = "後台使用者關閉：" + name
    else :
        status = 1
        log = "後台使用者啟用：" + name

    user.update(status=status)

    type = "編輯"
    Sor.objects.create(log=log, type=type)

    response = {'status': status}

    return JsonResponse(response)
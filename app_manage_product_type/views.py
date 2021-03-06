from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import uuid

from .models import Product_type
from app_system.models import System_operation_record as Sor
from app_manage_admin_user import user_decorator

father_title = "分類"
father_url = "manage_product_type_item_list"

# Create your views here.
@user_decorator.login
def item_list(request):
    if 'all' not in request.session['admin_premission'] and 'product' not in request.session['admin_premission']:
        return redirect('manage_home_home')

    search_text = request.GET.get('search_text', '')
    select_type = request.GET.get('select', '')

    product_type = Product_type.objects.filter(top_type__isnull=True).order_by('ordera')

    select_list = []
    for type in product_type:
        id = type.id
        title = type.title
        type.children_count = Product_type.objects.filter(top_type=id).count()
        type.label = '<span style="color:red">' + title + '</span>'
        select_list.append(type)

        select_list = get_type_children(id, select_list)
    type_list = select_list.copy()

    #下拉選單
    if select_type != '':
        try:
            product_type = Product_type.objects.get(id=select_type)
        except ObjectDoesNotExist or MultipleObjectsReturned:
            return redirect(item_list)

        type_list = []
        id = product_type.id
        title = product_type.title
        top_type = product_type.top_type
        product_type.children_count = Product_type.objects.filter(top_type=id).count()
        if top_type is not None:
            product_type.label = get_type_family_title(top_type, '<span style="color:red">' + title + '</span>')
        else:
            product_type.label = '<span style="color:red">' + title + '</span>'
        type_list.append(product_type)

        type_list = get_type_children(id, type_list)

    #搜尋文字
    if search_text!='':
        type_list = Product_type.objects.filter(title__icontains=search_text).order_by('ordera')
        for type in type_list:
            id = type.id
            top_type = type.top_type
            title = type.title
            type.children_count = Product_type.objects.filter(top_type=id).count()
            type.label = get_type_family_title(top_type, '<span style="color:red">' + title + '</span>')

    page = request.GET.get('page', 1)
    paginator = Paginator(type_list, 10)
    try:
        type_list = paginator.page(page)
    except PageNotAnInteger:
        type_list = paginator.page(1)
    except EmptyPage:
        type_list = paginator.page(paginator.num_pages)

    try:
        select_type=int(select_type)
    except ValueError:
        #print("ValueError")
        select_type=0

    #print(select_type)
    return render(request, 'manage/product_type/list.html', {
        'title': '分類',
        'select_list': select_list,
        'product_type': type_list,
        'search_text': search_text,
        'select_type': select_type,
    })

@user_decorator.login
def item_add(request):
    if 'all' not in request.session['admin_premission'] and 'product' not in request.session['admin_premission']:
        return redirect('manage_home_home')

    product_type = Product_type.objects.filter(top_type__isnull=True).order_by('ordera')
    select_list = []
    for type in product_type:
        top_type = type.top_type
        title = type.title
        type.label = '<span style="color:red">' + title + '</span>'  # get_type_family_title(None, '<span style="color:red">' + title + '</span>')
        select_list.append(type)

        id = type.id
        select_list = get_type_children(id, select_list)

    return render(request, 'manage/product_type/add.html', {
        'father_title': father_title,
        'father_url': father_url,
        'title': ' 新增分類',
        'select_list': select_list
    })

@user_decorator.login
def item_insert(request):
    if 'all' not in request.session['admin_premission'] and 'product' not in request.session['admin_premission']:
        return redirect('manage_home_home')
    if request.method == "POST":

        #print(request.POST)

        title = request.POST['title']
        top_type = request.POST['top_type']
        uid = uuid.uuid1().hex

        if top_type=="":
            top_type=None

        Product_type.objects.create(title=title, top_type=top_type, uid=uid)

        log = "新增分類：" + title
        type = "新增"
        Sor.objects.create(log=log, type=type)
        return HttpResponse("<script>parent.parent.alert('新增成功');parent.parent.window.location.href='"+reverse('manage_product_type_item_list')+"';</script>")#redirect(item_list)

@user_decorator.login
def item_edit(request, id=0):
    if 'all' not in request.session['admin_premission'] and 'product' not in request.session['admin_premission']:
        return redirect('manage_home_home')
    try:
        product_type = Product_type.objects.get(id=id)
    except ObjectDoesNotExist or MultipleObjectsReturned:
        return redirect(item_list)

    type_list = Product_type.objects.filter(top_type__isnull=True).order_by('ordera')
    select_list = []
    for type in type_list:
        top_type = type.top_type
        title = type.title
        type.label = '<span style="color:red">' + title + '</span>'  # get_type_family_title(None, '<span style="color:red">' + title + '</span>')
        select_list.append(type)

        id = type.id
        select_list = get_type_children(id, select_list)

    return render(request, 'manage/product_type/edit.html', {
        'father_title': father_title,
        'father_url': father_url,
        'title': ' 編輯分類',
        'product_type': product_type,
        'select_list': select_list
    })

@user_decorator.login
def item_update(request):
    if 'all' not in request.session['admin_premission'] and 'product' not in request.session['admin_premission']:
        return redirect('manage_home_home')
    if request.method == "POST":
        id = request.POST['id']
        title = request.POST['title']
        top_type = request.POST['top_type']
        if top_type=="":
            top_type=None

        product_type = Product_type.objects.filter(id=id)

        #不可移到子類別後
        check = check_move_to_child(id, top_type)
        print(check)
        if check:
            return HttpResponse("<script>parent.parent.alert('不可移到子類別後');</script>")

        product_type.update(title=title, top_type=top_type)

        log = "編輯分類：" + title
        type = "編輯"
        Sor.objects.create(log=log, type=type)
        return HttpResponse("<script>parent.parent.alert('編輯成功');parent.parent.window.location.href='"+reverse('manage_product_type_item_edit', kwargs={"id":id})+"';</script>")#redirect(item_edit, id=id)

@user_decorator.login
def item_delete(request, id=0):
    if 'all' not in request.session['admin_premission'] and 'product' not in request.session['admin_premission']:
        return redirect('manage_home_home')
    try:
        product_type = Product_type.objects.get(id=id)
    except ObjectDoesNotExist or MultipleObjectsReturned:
        return redirect(item_list)
    title = product_type.title

    product_type.delete()

    log = "刪除分類：" + title
    type = "刪除"
    Sor.objects.create(log=log, type=type)
    return redirect(item_list)

@user_decorator.login
def update_status(request):
    if 'all' not in request.session['admin_premission'] and 'product' not in request.session['admin_premission']:
        return redirect('manage_home_home')
    id      = request.POST['id']
    status  = request.POST['status']

    product_type = Product_type.objects.filter(id=id)
    title = product_type[0].title
    if status=='1':
        status = 0
        log = "分類下架：" + title
    else :
        status = 1
        log = "分類上架：" + title
    product_type.update(status=status)

    type = "編輯"
    Sor.objects.create(log=log, type=type)

    response = {'status': status}

    return JsonResponse(response)

def get_type_family_title(top_type, title=''):
    last_title = title
    #print(top_type, last_title)

    if top_type is not None:
        product_type = Product_type.objects.get(id=top_type)
        top_type = product_type.top_type
        title = product_type.title
        return get_type_family_title(top_type, title) + ">" + last_title

    return last_title

def get_type_children(id, type_list):
    product_type = Product_type.objects.filter(top_type=id).order_by('ordera')
    if product_type.count():
        for type in product_type:
            id = type.id
            top_type = type.top_type
            title = type.title
            type.children_count = Product_type.objects.filter(top_type=id).count()
            type.label = get_type_family_title(top_type, '<span style="color:red">' + title + '</span>')
            type_list.append(type)

            id = type.id
            type_list = get_type_children(id, type_list)

    return type_list

def check_move_to_child(id, top_type):
    id = int(id)
    if id == top_type:
        return True

    while True:
        try:
            product_type = Product_type.objects.get(id=top_type)
        except ObjectDoesNotExist or MultipleObjectsReturned:
            return False
        print(top_type)
        if id == top_type:
            return True
        top_type = product_type.top_type

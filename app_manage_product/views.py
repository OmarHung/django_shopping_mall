from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
import json

from upload_helper import Upload_helper

from .models import Product, Product_spec, Product_album
from app_system.models import System_operation_record as Sor
from app_manage_admin_user import user_decorator

father_title = "商品管理"
father_url = "manage_product_item_list"

# Create your views here.
@user_decorator.login
def item_list(request):
    if 'all' not in request.session['admin_premission'] and 'product' not in request.session['admin_premission']:
        return redirect('manage_home_home')
    #print(request.path)
    products = Product.objects.all()
    p = Product.objects.filter(id__gte=2)
    #print(products.query)
    search_text = request.GET.get('search_text', '')
    if search_text!='':
        products = Product.objects.filter(title__icontains=search_text)

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 10)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'manage/product/product_list.html', {
        'title': '商品管理',
        'products': products,
        'search_text': search_text,
    })

@user_decorator.login
def item_add(request):
    if 'all' not in request.session['admin_premission'] and 'product' not in request.session['admin_premission']:
        return redirect('manage_home_home')
    return render(request, 'manage/product/product_add.html', {
        'father_title': father_title,
        'father_url': father_url,
        'title': ' 新增商品',
    })

@user_decorator.login
def item_insert(request):
    if 'all' not in request.session['admin_premission'] and 'product' not in request.session['admin_premission']:
        return redirect('manage_home_home')
    if request.method == "POST":

        print(request.POST)

        title = request.POST['title']
        ori_price = request.POST['ori_price']
        sale_price = request.POST['sale_price']

        Product.objects.create(title=title, ori_price=ori_price, sale_price=sale_price)

        id = Product.objects.latest('id').id

        spec_1 = request.POST.getlist('spec_1[]')
        # print(spec_1)
        spec_2 = request.POST.getlist('spec_2[]')
        # print(spec_2)
        stock = request.POST.getlist('stock[]')
        # print(stock)

        product_spec = Product_spec.objects.filter(product_id=id)
        product_spec.delete()
        for index in range(len(spec_1)):
            Product_spec.objects.create(product_id=id, spec_1=spec_1[index], spec_2=spec_2[index], stock=stock[index])

        if request.FILES:
            uh = Upload_helper(request, 'product')
            imgs_data = uh.upload_multi_image(config = {'input_name': 'files'})

            for img in imgs_data:
                Product_album.objects.create(product_id=id, img_url=img['file_url'], ori_name=img['ori_name'], name=img['name'], file_type=img['type'], file_size=img['size'], ordera=img['index'])

        log = "新增商品：" + title
        type = "新增"
        Sor.objects.create(log=log, type=type)
        return redirect(item_list)

@user_decorator.login
def item_edit(request, id=0):
    if 'all' not in request.session['admin_premission'] and 'product' not in request.session['admin_premission']:
        return redirect('manage_home_home')
    try:
        imgs_json = []

        product = Product.objects.get(id=id)
        spec = Product_spec.objects.filter(product_id=product.id)
        album = Product_album.objects.filter(product_id=product.id).order_by('ordera')

        for img in album:
            imgs_json.append({
                'img_id': str(img.id),
                'name': img.name,
                'type': img.file_type,
                'size': str(img.file_size),
                'file': img.img_url,
                'data': {
                    'url': img.img_url,
                    'thumbnail': None,
                },
            })

    except ObjectDoesNotExist or MultipleObjectsReturned:
        return redirect(item_list)


    return render(request, 'manage/product/product_edit.html', {
        'father_title': father_title,
        'father_url': father_url,
        'title': ' 編輯商品',
        'product': product,
        'spec': spec,
        'imgs_json': json.dumps(imgs_json)
    })

@user_decorator.login
def item_update(request):
    if 'all' not in request.session['admin_premission'] and 'product' not in request.session['admin_premission']:
        return redirect('manage_home_home')
    if request.method == "POST":
        id = request.POST['id']
        title = request.POST['title']
        ori_price = request.POST['ori_price']
        sale_price = request.POST['sale_price']

        product = Product.objects.filter(id=id)
        product.update(title=title, ori_price=ori_price, sale_price=sale_price)

        spec_1 = request.POST.getlist('spec_1[]')
        #print(spec_1)
        spec_2 = request.POST.getlist('spec_2[]')
        #print(spec_2)
        stock = request.POST.getlist('stock[]')
        #print(stock)

        product_spec = Product_spec.objects.filter(product_id=id)
        product_spec.delete()
        for index in range(len(spec_1)):
            Product_spec.objects.create(product_id=id, spec_1=spec_1[index], spec_2=spec_2[index], stock=stock[index])

        log = "編輯商品：" + title
        type = "編輯"
        Sor.objects.create(log=log, type=type)
        return redirect(item_edit, id=id)

@user_decorator.login
def item_delete(request, id=0):
    if 'all' not in request.session['admin_premission'] and 'product' not in request.session['admin_premission']:
        return redirect('manage_home_home')
    try:
        product = Product.objects.get(id=id)
    except ObjectDoesNotExist or MultipleObjectsReturned:
        return redirect(item_list)
    title = product.title

    product.delete()

    product_spec = Product_spec.objects.filter(product_id=id)
    product_spec.delete()

    product_album = Product_album.objects.filter(product_id=id)
    for img_data in product_album:
        img = img_data.name
        fs = FileSystemStorage()
        fs.delete('product/' + img)
    product_album.delete()

    log = "刪除商品：" + title
    type = "刪除"
    Sor.objects.create(log=log, type=type)
    return redirect(item_list)

@user_decorator.login
def update_status(request):
    if 'all' not in request.session['admin_premission'] and 'product' not in request.session['admin_premission']:
        return redirect('manage_home_home')
    id      = request.POST['id']
    status  = request.POST['status']

    product = Product.objects.filter(id=id)
    title = product[0].title
    if status=='1':
        status = 0
        log = "商品下架：" + title
    else :
        status = 1
        log = "商品上架：" + title
    product.update(status=status)

    type = "編輯"
    Sor.objects.create(log=log, type=type)

    response = {'status': status}

    return JsonResponse(response)

@user_decorator.login
def ajax_upload_images(request):
    if request.method == "POST":
        id = request.POST['id']

        product = Product.objects.filter(id=id)
        title = product[0].title

        index = Product_album.objects.filter(product_id=id).count()

        if request.FILES:
            uh = Upload_helper(request, 'product')
            img = uh.ajax_upload_imgs(config = {'input_name': 'files'})

            Product_album.objects.create(product_id=id, img_url=img['files'][0]['file'], ori_name=img['files'][0]['old_name'], name=img['files'][0]['name'], file_type=img['files'][0]['type'], file_size=img['files'][0]['size'], ordera=index)

        log = "新增商品圖片：" + title
        type = "新增"
        Sor.objects.create(log=log, type=type)

        #del img['thumbnail_url']

        return HttpResponse(json.dumps(img), content_type='text/html; charset=UTF-8')

@user_decorator.login
def ajax_sorter_img(request):
    if request.method == "POST":
        list = json.loads(request.POST['_list'])
        #print(list)
        for val in list:
            #print(val)
            picture = Product_album.objects.filter(name=val['name'])
            picture.update(ordera=val['index'])

        response = {'status': '201'}

        return JsonResponse(response)

@user_decorator.login
def ajax_delete_img(request):
    if request.method == "POST":
        response = {}

        img = request.POST['file']
        Product_album.objects.filter(name=img).delete()

        fs = FileSystemStorage()
        fs.delete('product/' + img)
        #fs.delete('product/s_' + img)

        response['status'] = 200
        response['msg'] = "刪除成功"

        # response['status'] = 501
        # response['msg'] = "error!"
        return JsonResponse(response)

@user_decorator.login
def ajax_crop_img(request):
    if request.method == "POST":
        uh = Upload_helper(request, 'product')
        uh.crop_image()

        response = {'status': '201'}

        return JsonResponse(response)

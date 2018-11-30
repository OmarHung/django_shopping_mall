from django.urls import include, path
from app_manage_product import views as manage_product

urlpatterns = [
    path('item_list/', manage_product.item_list, name='manage_product_item_list'),
    path('item_add/', manage_product.item_add, name='manage_product_item_add'),
    path('item_edit/<int:id>', manage_product.item_edit, name='manage_product_item_edit'),
    path('update_status/', manage_product.update_status, name='manage_product_update_status'),
    path('item_insert/', manage_product.item_insert, name='manage_product_item_insert'),
    path('item_update/', manage_product.item_update, name='manage_product_item_update'),
    path('item_delete/', manage_product.item_delete, name='manage_product_item_delete1'),
    path('item_delete/<int:id>', manage_product.item_delete, name='manage_product_item_delete2'),
    path('ajax_upload_images/', manage_product.ajax_upload_images, name='ajax_upload_images'),
    path('ajax_sorter_img/', manage_product.ajax_sorter_img, name='ajax_sorter_img'),
    path('ajax_delete_img/', manage_product.ajax_delete_img, name='ajax_delete_img'),
    path('ajax_crop_img/', manage_product.ajax_crop_img, name='ajax_crop_img'),
]
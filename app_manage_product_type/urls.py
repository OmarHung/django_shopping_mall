from django.urls import include, path
from app_manage_product_type import views as manage_product_type

urlpatterns = [
    path('item_list/', manage_product_type.item_list, name='manage_product_type_item_list'),
    path('item_add/', manage_product_type.item_add, name='manage_product_type_item_add'),
    path('item_edit/<int:id>', manage_product_type.item_edit, name='manage_product_type_item_edit'),
    path('update_status/', manage_product_type.update_status, name='manage_product_type_update_status'),
    path('item_insert/', manage_product_type.item_insert, name='manage_product_type_item_insert'),
    path('item_update/', manage_product_type.item_update, name='manage_product_type_item_update'),
    path('item_delete/', manage_product_type.item_delete, name='manage_product_type_item_delete1'),
    path('item_delete/<int:id>', manage_product_type.item_delete, name='manage_product_type_item_delete2'),
]
from django.urls import include, path
from app_manage_admin_user import views as manage_admin_user

urlpatterns = [
    path('item_list/', manage_admin_user.item_list, name='manage_admin_user_item_list'),
    path('item_add/', manage_admin_user.item_add, name='manage_admin_user_item_add'),
    path('item_insert/', manage_admin_user.item_insert, name='manage_admin_user_item_insert'),
    path('item_edit/<int:id>', manage_admin_user.item_edit, name='manage_admin_user_item_edit'),
    path('item_update/', manage_admin_user.item_update, name='manage_admin_user_item_update'),
    path('update_status/', manage_admin_user.update_status, name='manage_admin_user_update_status'),
    path('item_delete/', manage_admin_user.item_delete, name='manage_admin_user_item_delete1'),
    path('item_delete/<int:id>', manage_admin_user.item_delete, name='manage_admin_user_item_delete2'),
]
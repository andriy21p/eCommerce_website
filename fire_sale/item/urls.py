from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='item-index'),
    path('<int:item_key>', views.get_item_by_id),
    path('<int:item_key>/edit', views.edit, name='item-edit'),
    path('create', views.create, name='item-create'),
]

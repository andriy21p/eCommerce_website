from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='item-index'),
    path('<int:item_key>', views.get_item_by_id),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='checkout'),
    path('<int:order_id>', views.index),
    # path('create', views.register_checkout, ame='create-checkout'),
]

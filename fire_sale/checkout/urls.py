from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='checkout'),
    # path('<int:msg_key>', views.get_msg_by_id),
    # path('create', views.register_checkout, name='create-checkout'),
]

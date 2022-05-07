from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='message'),
    path('<int:msg_key>', views.get_msg_by_id),
    path('create', views.create_new_msg, name='create-new-message'),
    path('<int:msg_key>/accept', views.accept_bid, name='accept-offer'),
    path('<int:msg_key>/reject', views.reject_bid, name='reject-offer')
]

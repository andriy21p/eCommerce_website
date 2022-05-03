from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='message'),
    path('message/new/', views.create_new_msg, name='create-new-message'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='message'),
    path('<int:msg_key>', views.get_msg_by_id),
    path('create/<int:to_user_id>', views.create_new_msg, name='create-new-message'),
    path('<int:msg_key>/reply', views.msg_reply, name='reply-message'),
    path('<int:msg_key>/accept', views.accept_bid, name='accept-offer'),
    path('<int:msg_key>/reject', views.reject_bid, name='reject-offer'),
    path('number_of_unread', views.number_of_unread, name='number_of_unread'),
    path('message-fire-sale', views.msg_admin, name='message-admins'),
]

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='my-profile'),
    path('<int:user_id>', views.other_profile, name='other-profile'),
    path('register', views.register, name='register'),
    path('login', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('profile', views.profile, name='profile'),
    path('image', views.image, name='profile-image'),
]

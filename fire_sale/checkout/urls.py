from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='checkout'),
    path('<int:order_id>', views.register_checkout, name="register-checkout"),
    path('<int:checkout_id>/preview', views.get_checkout_by_id, name="preview"),
    path('<int:checkout_id>/confirm', views.checkout_complete, name="confirm-checkout"),
    path("<int:checkout_id>/review", views.user_review, name="review")
]

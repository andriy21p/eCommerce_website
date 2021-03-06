from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='item-index'),
    path('create', views.create, name='item-create'),
    path('<int:item_key>', views.get_item_by_id),
    path('<int:item_key>/edit', views.edit, name='item-edit'),
    path('<int:item_key>/bid', views.bid, name='item-bid'),
    path('<int:item_key>/offers', views.offers, name='item-bid'),
    path('<int:item_key>/delete', views.delete, name='delete-item'),
    path('offer/<int:offer_id>/accept', views.accept_item_bid, name='offer-accept'),
    path('<int:item_key>/similar', views.similar, name='similar-items'),
    path('<int:item_key>/addimage', views.addimage, name='item-addimage'),
    path('<int:item_key>/<int:image_key>/removeimage', views.removeimage, name='item-removeimage'),
]

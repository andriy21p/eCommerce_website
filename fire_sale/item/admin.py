from django.contrib import admin
from item.models import *

# Register your models here.

admin.site.register(Item)
admin.site.register(ItemCondition)
admin.site.register(ItemSalesType)
admin.site.register(ItemCategory)
admin.site.register(ItemImage)
admin.site.register(Offer)
admin.site.register(Tag)

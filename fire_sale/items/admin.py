from django.contrib import admin
from items.models import *

# Register your models here.

admin.site.register(Items)
admin.site.register(ItemCondition)
admin.site.register(ItemsSalesType)
admin.site.register(ItemCategory)

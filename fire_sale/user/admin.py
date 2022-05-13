from django.contrib import admin
from user.models import *

# Register your models here.


class FooterLinksAdmin(admin.ModelAdmin):
    list_display = ('get_footer_page', 'created')

    def get_footer_page(self, obj):
        return obj.get_footer_page_display()

    get_footer_page.short_description = "Footer Type"


admin.site.register(Profile)
admin.site.register(Footer, FooterLinksAdmin)




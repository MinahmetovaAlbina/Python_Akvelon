from django.contrib import admin


from .models import MyUrl


class TinyUrlAdmin(admin.ModelAdmin):
    list_display = ('original_url', 'tiny_url', 'num_of_uses')
    search_fields = ['original_url']
    list_filter = ['num_of_uses']


admin.site.register(MyUrl, TinyUrlAdmin)
admin.AdminSite.site_header = 'Tiny URL Administrations'
admin.AdminSite.site_title = 'Tiny URL'


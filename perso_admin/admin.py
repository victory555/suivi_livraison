from django.contrib import admin

from .models import Admin
# Register your models here.
class AdminAdmin(admin.ModelAdmin):
    list_display=["email", "username"]
    search_fields=["email", "username"]
admin.site.register(Admin, AdminAdmin)
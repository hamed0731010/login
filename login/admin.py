from django.contrib import admin
from .models import User,Log
# Register your models here.
admin.site.register(User)

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display=['num','type_log','time_log',]
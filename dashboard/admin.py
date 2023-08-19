from django.contrib import admin

from .models import MyFileManager

class MyFileManagerAdmin(admin.ModelAdmin):
    list_display = ('ids', 'file_name', 'file_upload_date',)



admin.site.register(MyFileManager, MyFileManagerAdmin)

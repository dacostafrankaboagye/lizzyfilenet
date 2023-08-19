
from django import forms
from .models import MyFileManager


class MyFileManagerForm(forms.ModelForm):
    class Meta:
        model = MyFileManager
        fields = ('file_name', 'file_description', 'file_type', 'my_file')
        


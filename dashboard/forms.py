
from django import forms
from .models import MyFileManager



class MyFileManagerForm(forms.ModelForm):
    class Meta:
        model = MyFileManager
        fields = ('file_name', 'file_description', 'file_type', 'my_file')
        
class ShareFileForm(forms.Form):

    email = forms.EmailField(required=True)
    subject = forms.CharField(required=False)
    message = forms.CharField(required=False)
    
    # email = forms.EmailField(
    #     widget=forms.PasswordInput(attrs={
    #         'name': 'email',
    #         'type': 'email',
    #         'class': 'input',
    #         'id': 'email',
    #         'required': '',
    #         }
    #     ),  
    # )




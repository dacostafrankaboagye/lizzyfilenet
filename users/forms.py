from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):

  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({
            'name': 'email',
            'type': 'text',
            'class': 'input',
            'id': 'email',
            'required': '',
            'autocomplete': 'off',
        })
        self.fields["password1"].widget.attrs.update({
            'name': 'password1',
            'type': 'password',
            'class': 'input',
            'id': 'password1',
            'required': '',
        })
        self.fields["password2"].widget.attrs.update({
            'name': 'password2',
            'type': 'password',
            'class': 'input',
            'id': 'password2',
            'required': '',
        })
    

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user

'''
self.fields["username"].widget.attrs.update({
            'name': 'username',
            'type': 'text',
            'class': 'input',
            'id': 'username',
        })

'''
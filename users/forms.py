


from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm

from django.contrib.auth import get_user_model

#from django.contrib.auth.models import User

class UserRegisterationForm(UserCreationForm):
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


    username = forms.CharField( required=False)
    email = forms.EmailField(required=True)
    

    class Meta:
        model = get_user_model()
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegisterationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email'] 
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'name': 'username',
            'type': 'text',
            'class': 'input',
            'id': 'username',
            'required': '',
        })
        self.fields["password"].widget.attrs.update({
            'name': 'password',
            'type': 'password',
            'class': 'input',
            'id': 'password',
            'required': '',
        })
        

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['username','email', 'profilePicture']



# class SetPasswordForm(SetPasswordForm):
    
#     def __init__(self, *args, **kwargs):
#         super(SetPasswordForm, self).__init__(*args, **kwargs)

#     new_password1 = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'name': 'new_password1',
#             'type': 'password',
#             'class': 'input',
#             'id': 'new_password1',
#             'required': '',
#             }
#         ),
#     )
#     new_password2 = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'name': 'new_password2',
#             'type': 'password',
#             'class': 'input',
#             'id': 'new_password2',
#             'required': '',
#             }
#         ),
#     )

class SetPasswordForm(SetPasswordForm):
    
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'name': 'new_password1',
            'type': 'password',
            'class': 'input',
            'id': 'new_password1',
            'required': '',
            }
        ),
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'name': 'new_password2',
            'type': 'password',
            'class': 'input',
            'id': 'new_password2',
            'required': '',
            }
        ),
    )     



class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'name': 'email',
            'type': 'text',
            'class': 'input',
            'id': 'email',
            'required': '',
            "autocomplete": "email"
        }),
    )

    
        


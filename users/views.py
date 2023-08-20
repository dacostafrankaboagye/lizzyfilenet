from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import SignUpForm

from django.contrib.auth import authenticate, login


def signup(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            #instance.username = 'the_default_user'
            
            login(request=request, user=user)
            return redirect('dashboard-index')
            # theEmail = form.cleaned_data.get("email")
            # thePassword1 = form.cleaned_data.get("password1")
            # thePassword2 = form.cleaned_data.get("password2")
            #form.save()
            # new_user = authenticate(
            #     username='', 
            #     email=theEmail, 
            #     password=thePassword1
            # )
            # if new_user is not None:
            #     login(request=request, user=new_user)
            #     return redirect('dashboard-index')
            # else:
            #     return HttpResponse(' new user is none ')
        else:
            return HttpResponse(" form is not valid")

   
    form = SignUpForm()

    context = {
        'form': form,
    }
    return render(
        request=request,
        template_name='users/signup.html',
        context=context,
    )

from django.shortcuts import HttpResponse, render, redirect

from django.contrib.auth import get_user_model, login, logout, authenticate
from .forms import UserRegisterationForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm





def register(request):
    if request.method == "POST":
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request=request, user=user)
            messages.success(request=request, message=f'new account created for { user.email }')
            return redirect('dashboard-index')
        else:
            # allerror = ''
            for error in list(form.errors.values()): 
                # print(request, error)
                # allerror = allerror + error + "---"
                messages.error(request, error)
                
            # return HttpResponse(allerror) 
    else:
        form = UserRegisterationForm()

    return render(
        request=request,
        template_name='users/signup.html',
        context={'form': form}
    )




def custom_logout(request):
    logout(request=request)
    return render(request, template_name='users/logout.html')


def custom_login(request):

    if request.method == 'POST':
        #form  = AuthenticationForm(request=request, data=request.POST)
        form  = UserLoginForm(request=request, data=request.POST)
        
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
            )
            if user is not None:
                login(request=request, user=user)
                messages.success(request=request, message=f"Hello <b>{ user.username }</b>!. You have been logged in ")
                return redirect('dashboard-index')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)


    
    form = UserLoginForm()

    return render(
        request=request,
        template_name='users/login.html',
        context={'form': form}
    )



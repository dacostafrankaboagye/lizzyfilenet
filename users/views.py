from django.shortcuts import HttpResponse, render, redirect

from django.contrib.auth import get_user_model, login, logout, authenticate
from .forms import UserRegisterationForm, UserLoginForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.decorators import login_required



def register(request):
    if request.method == "POST":
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            #user = form.save()
            #login(request=request, user=user)
            #messages.success(request=request, message=f'new account created for { user.email }')
            #return redirect('login')
            form.save()
            return redirect('login')
        else:
            allerror = ' '
            for error in list(form.errors.values()): 
                # print(request, error)
                allerror = allerror + error + "---"
                #messages.error(request, error)
            return HttpResponse(allerror) 
    else:
        form = UserRegisterationForm()

    return render(
        request=request,
        template_name='users/signup.html',
        context={'form': form}
    )


@login_required
def custom_logout(request):
    logout(request=request)
    return render(request, template_name='users/logout.html')


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard-index')

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
                #messages.success(request=request, message=f"Hello <b>{ user.username }</b>!. You have been logged in ")
                return redirect('dashboard-index')
        else:
            # for error in list(form.errors.values()):
            #     messages.error(request, error)
            allerror = ' '
            for error in list(form.errors.values()):
                allerror = allerror + error + "---"
            return HttpResponse(allerror) 


    
    form = UserLoginForm()

    return render(
        request=request,
        template_name='users/login.html',
        context={'form': form}
    )


@login_required
def profilepage(request):
    return render(
        request=request,
        template_name='users/profilepage.html'
    )

@login_required
def profilepageUpdate(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profilepage')
    else:
        form = UserUpdateForm(instance=request.user)

    
    
    context = {
        'form': form,
    }
    return render(
        request=request,
        template_name='users/profilepageUpdate.html',
        context=context
    )

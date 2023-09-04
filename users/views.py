from django.shortcuts import HttpResponse, render, redirect

from django.contrib.auth import get_user_model, login, logout, authenticate
from .forms import UserRegisterationForm, UserLoginForm, UserUpdateForm, PasswordResetForm, SetPasswordForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.decorators import login_required

#forEmail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import activationToken

from django.db.models import Q



def activateEmail(request, uidb64, token):
    user = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        theUser = user.objects.get(pk=uid)
    except:
        theUser = None
    
    if theUser is not None and activationToken.check_token(theUser, token):
        theUser.is_active = True
        theUser.save()

        messages.success(
            request=request,
            message='Email Confirmed!. Now you can log in now',
        )
        return redirect('login')
    else:
        messages.error(
            request=request,
            message='Invalid Link',
        )

    return redirect('register')


def userEmailActivation(request, theUser, theUserEmail):
    theSubject = 'Account Activation for Lizzy File Net'
    context={
        'user': theUser ,
        'protocol': 'https' if request.is_secure() else 'http' ,
        'domain': get_current_site(request=request).domain ,
        'uid': urlsafe_base64_encode(force_bytes(theUser.pk)),
        'token': activationToken.make_token(theUser),
    }
    theMessage = render_to_string(
        template_name='users/Template_userEmailActivation.html',
        context=context,        
    )

    theEmail = EmailMessage(
        subject=theSubject,
        body=theMessage,
        to=[theUserEmail],
    )

    if theEmail.send():  # True is if it sends
        messages.success(
            request=request,
            message=f'Please Go to your email {theUserEmail} to complete registration'
        )
    else:
        messages.error(
            request=request,
            message=f'Encountered a problem while sending email to {theUserEmail}. Check the spelling'
        )
    

def register(request):

    if request.method == "POST":
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            theUser = form.save(commit=False)
            theUser.is_active = False
            theUser.save()

            userEmailActivation(
                request=request,
                theUser=theUser, 
                theUserEmail=form.cleaned_data.get('email')
            )

            return redirect('login')
        else:
            allerror = ' '
            for error in list(form.errors.values()): 
                # print(request, error)
                allerror = allerror + error + "---"
                #messages.error(request, error)
            allerror += '==> from- form is not valid - register function'
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


def passwordResetRequest(request):

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            theUserEmail = form.cleaned_data['email']
            theUser = get_user_model().objects.filter(Q(email=theUserEmail)).first()

            if theUser:
                theSubject = "Reset Your Password"

                context = {
                    'user': theUser,
                    "protocol": 'https' if request.is_secure() else 'http',
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(theUser.pk)),
                    'token': activationToken.make_token(theUser),                  
                }

                theMessage = render_to_string(
                    template_name="users/Template_passwordResetRequest.html", 
                    context=context,
                )

                theEmail = EmailMessage(
                    subject=theSubject,
                    body=theMessage,
                    to=[theUserEmail],
                )

                if theEmail.send():
                    messages.success(
                        request=request,
                        message='Password reset sent to your email'
                    )
                else:
                    messages.error(
                        request=request, 
                        message="Problem sending reset password email"
                    )

            return redirect('login')

        else:
            allerror = ''
            for error in list(form.errors.values()):
                allerror = allerror + error + "---"
            return HttpResponse(allerror) 

    form = PasswordResetForm()
    context = {
        "form": form,
    }
    return render(
        request=request, 
        template_name="users/passwordResetRequest.html", 
        context=context,
    )


def passwordResetConfirm(request, uidb64, token):

    user = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        theUser = user.objects.get(pk=uid)
    except:
        theUser = None

    if theUser is not None and activationToken.check_token(theUser, token):
        if request.method == 'POST':
            form = SetPasswordForm(theUser, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. Log in now.")
                return redirect('login')
            else:
                allerror = '->'
                for error in list(form.errors.values()):
                    allerror += error 
                allerror += ": passwordResetConfirm Fnx"
                return HttpResponse(allerror) 

        form = SetPasswordForm(theUser)
        context = {
            'form': form,
        }

        return render(
            request=request, 
            template_name='users/passwordResetConfirm.html',
            context=context,
        )
    else:
        messages.error(
            request=request, 
            message="Invalid Link: passwordResetConfirm"
        )

    
    return redirect('register')


















'''
# old

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

    

    def changePassword(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request=request,
                message='Password has been changed.!!'
            )
            return redirect('login')
        else:
            allerror = '->'
            for error in list(form.errors.values()):
                allerror = allerror + error
            allerror += ':: password form is not valid'
            return HttpResponse(allerror) 
    else:
        form = SetPasswordForm(user)
    context = {
        'form': form,
    }
    return render(
        request=request,
        template_name='users/confirmPasswordReset.html',
        context = context,
    )

'''
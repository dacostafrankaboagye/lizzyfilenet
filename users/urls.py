from django.urls import path

from . import views

#from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register' ),
    path('', views.custom_login, name='login' ),
    path('logout/', views.custom_logout, name='logout' ),
    path('profilepage/', views.profilepage, name='profilepage' ),
    path('profilepageUpdate/', views.profilepageUpdate, name='profilepageUpdate' ),
    path('activateEmail/<uidb64>/<token>/', views.activateEmail, name='activateEmail' ),
    #path("changePassword/", views.changePassword, name="changePassword"),
    path("passwordResetRequest/", views.passwordResetRequest, name="passwordResetRequest"),
    path('passwordResetConfirm/<uidb64>/<token>/', views.passwordResetConfirm, name='passwordResetConfirm'),
    

]

    #path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login' ),
    # path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout' ),

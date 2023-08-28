
from django.urls import path
from . import views

urlpatterns = [

    path('dashboard/', views.index, name='dashboard-index'),
    path('admin_panel/', views.admin_panel, name="admin_panel" ),
    path('file_delete/<pk>/', views.file_delete, name="file_delete" ),
    path('file_update/<pk>/', views.file_update, name="file_update" ),
    
]

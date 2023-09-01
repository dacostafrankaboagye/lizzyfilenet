
from django.urls import path
from . import views

urlpatterns = [

    path('dashboard/', views.index, name='dashboard-index'),
    path('admin_panel/', views.admin_panel, name="admin_panel" ),
    path('file_delete/<pk>/', views.file_delete, name="file_delete" ),
    path('file_update/<pk>/', views.file_update, name="file_update" ),

    path('specificFiles/all/', views.specificFiles, name="specificFiles_all" ),
    path('specificFiles/pdf/', views.specificFiles, name="specificFiles_pdf" ),
    path('specificFiles/image/', views.specificFiles, name="specificFiles_image" ),
    path('specificFiles/audio/', views.specificFiles, name="specificFiles_audio" ),
    path('specificFiles/video/', views.specificFiles, name="specificFiles_video" ),
    path('specificFiles/other/', views.specificFiles, name="specificFiles_other" ),

    
]

from django.shortcuts import render

# code
from .models import  MyFileManager
from .forms import MyFileManagerForm



def index(request):

    the_files = MyFileManager.objects.all()

    context = {
        'the_files': the_files,
    }

    return render(
        request=request,
        template_name='dashboard/index.html',
        context=context
    )

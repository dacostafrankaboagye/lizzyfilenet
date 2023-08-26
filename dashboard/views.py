from django.shortcuts import render, redirect

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


def admin_panel(request):
    the_files = MyFileManager.objects.all()
    if request.method == "POST":
        form  = MyFileManagerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = MyFileManagerForm()
    context = {
        'the_files': the_files,
        'form': form,
    }
    return render(
        request=request,
        template_name='dashboard/admin_panel.html',
        context=context
    )
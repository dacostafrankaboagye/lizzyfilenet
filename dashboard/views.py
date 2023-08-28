from django.shortcuts import render, redirect

# code
from .models import  MyFileManager
from .forms import MyFileManagerForm

from django.contrib.auth.decorators import login_required


@login_required
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

@login_required
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

def file_delete(request, pk):
    the_file = MyFileManager.objects.get(ids=pk)
    if request.method == 'POST':
        the_file.delete()
        return redirect('admin_panel')
        
    context = {
        'the_file': the_file,
    }
    return render(
        request=request,
        template_name='dashboard/file_delete.html',
        context=context,
    )

def file_update(request, pk):
    the_file = MyFileManager.objects.get(ids=pk)
    if request.method == 'POST':
        form  = MyFileManagerForm(request.POST, request.FILES, instance=the_file)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form  = MyFileManagerForm(instance=the_file)
        
        
    context = {
        'form': form,
    }
    return render(
        request=request,
        template_name='dashboard/file_update.html',
        context=context,
    )
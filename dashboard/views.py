from django.shortcuts import render, redirect

# code
from .models import  MyFileManager
from .forms import MyFileManagerForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect

@login_required
def index(request):
    
    if 'q' in request.GET:
        q = request.GET['q']
        the_files = MyFileManager.objects.filter(file_name__icontains=q)
        # multiple_q = Q(Q(first_name__icontains=q) | Q(last_name__icontains=q)  )
        # the_files = MyFileManager.objects.filter(multiple_q)
    else:
        the_files = MyFileManager.objects.all()

    context = {
        'the_files': the_files,
        'urlFileType': "all",
    }
    return render(
        request=request,
        template_name='dashboard/index.html',
        context=context
    )

@login_required
def specificFiles(request):
    if 'q' in request.GET:
        q = request.GET['q']
        the_files = MyFileManager.objects.filter(file_name__icontains=q)
    else:
        the_files = MyFileManager.objects.all()

    
    theUrl = request.build_absolute_uri()
    urlFileType = theUrl.split('/')[-2]  # getting the specific
    context = {
        'the_files': the_files,
        'urlFileType': urlFileType,
    }
    return render(
        request=request,
        template_name='dashboard/index.html',
        context = context,
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

@login_required
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

@login_required
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

@login_required
def preview(request, pk):
    the_file = MyFileManager.objects.get(ids=pk)

    if the_file.file_type == 'pdf' or the_file.file_type == 'other':
        return HttpResponseRedirect(the_file.my_file.url)


    context = {
        'the_file': the_file,
    }

    return render(
        request=request,
        template_name='dashboard/preview.html',
        context=context,
    )



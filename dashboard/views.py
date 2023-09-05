from django.shortcuts import render, redirect

# code
from .models import  MyFileManager
from .forms import MyFileManagerForm, ShareFileForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from users.models import CustomUser

from django.core.mail import EmailMessage
from django.contrib import messages


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


def calculateDownloadTotal(the_files):
    emailTotal = 0
    downloadTotal = 0
    for the_file in the_files:
        emailTotal += the_file.emailCount
        downloadTotal += the_file.downloadCount

    return [emailTotal, downloadTotal]


@login_required
def admin_panel(request):

    the_files = MyFileManager.objects.all()
    totalUsers = CustomUser.objects.all().count()
    totalNumberOfDownloads = calculateDownloadTotal(the_files)    

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
        'totalUsers': totalUsers,
        'emailTotal': totalNumberOfDownloads[0],        
        'downloadTotal': totalNumberOfDownloads[1],        
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


@login_required
def fileDownload(request, pk):
    the_file = MyFileManager.objects.get(ids=pk)
    the_file.downloadCount += 1
    the_file.save()
    context = {
        'the_file': the_file,
    }
    return render(
        request=request,
        template_name='dashboard/fileDownload.html',
        context=context,
    )


@login_required
def shareFile(request, pk):

    the_file = MyFileManager.objects.get(ids=pk)
    
    if request.method == 'POST':
        form = ShareFileForm(request.POST)
        theErrorMessage = ''
        if form.is_valid():
            theRecipientEmail = form.cleaned_data['email']
            theRecipientSubject = form.cleaned_data['subject']
            theRecipientMessage = form.cleaned_data['message']
            if theRecipientEmail:
                theSubject = theRecipientSubject 
                theMessage = theRecipientMessage
                theEmail = EmailMessage(
                    subject=theSubject,
                    body=theMessage,
                    to=[theRecipientEmail],
                )
                try:
                    theEmail.attach(the_file.my_file.name, the_file.my_file.read())                
                    if theEmail.send():
                        context = {'theRecipientEmail': theRecipientEmail,}
                        the_file.emailCount += 1
                        the_file.save()
                        return render(
                            request=request,
                            template_name='dashboard/fileSent.html',
                            context=context,
                        )  
                except:
                    theErrorMessage="Problem sending email- Either Attachment or File Size"        
            else:
                theErrorMessage="Problem sending email - The Recipient Email"    
        else:
            theErrorMessage="Problem with Form"
        
    
        return render(
            request=request,
            template_name='information.html',
            context = {'theErrorMessage':theErrorMessage,}
        )

    form = ShareFileForm()
    context = {
        'form': form,
    }
    return render(
        request=request,
        template_name='dashboard/shareFile.html',
        context=context,
    )




from django.db import models

MYFILETYPES = (
    ('pdf', 'pdf'),
    ('image', 'image'),
    ('audio', 'audio'),
    ('video', 'video'),
    ('other', 'other'),
)

the_code = {
    'pdf'   : ('danger',  'bi-filetype-pdf'),
    'image' : ('primary', 'bi-images'),
    'audio' : ('warning', 'bi-file-earmark-music'),
    'video' : ('success', 'bi-file-earmark-play'),
    'other' : ('primary', 'bi-file-earmark')
} 


class MyFileManager(models.Model):
    file_name = models.CharField(max_length=200, default="File", blank=False)  # title
    file_description = models.TextField(default='This is a File', max_length=200, blank=False) # description
    file_type = models.CharField(max_length=20, choices=MYFILETYPES)
    my_file = models.FileField(upload_to="all_files")
    ids = models.AutoField(primary_key=True)
    file_upload_date =  models.DateTimeField(auto_now_add=True)
    downloadCount = models.PositiveIntegerField(default=0, blank=True)
    emailCount = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        return self.file_name
    
    def get_color_code(self):
        return the_code[self.file_type][0]
    
    def get_icon(self):
        return the_code[self.file_type][1]


    
    class Meta:
        ordering = ('-file_upload_date',)



    


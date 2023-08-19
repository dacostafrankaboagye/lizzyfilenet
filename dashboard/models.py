from django.db import models



MYFILETYPES = (
    ('pdf', 'pdf'),
    ('image', 'image'),
    ('audio', 'audio'),
    ('video', 'video'),
    ('other', 'other'),
)

color_code = {
    'pdf'   : 'danger',
    'image' : 'primary',
    'audio' : 'warning',
    'video' : 'success',
    'other' : 'primary'
}

class MyFileManager(models.Model):
    file_name = models.CharField(max_length=200, default="File", blank=False)  # title
    file_description = models.TextField(default='This is a File', max_length=600, blank=False) # description
    file_type = models.CharField(max_length=20, choices=MYFILETYPES)
    my_file = models.FileField(upload_to="all_files")
    ids = models.AutoField(primary_key=True)
    file_upload_date =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
    
    def get_color_code(self):
        return color_code[self.file_type]
    
    class Meta:
        ordering = ('-file_upload_date',)

    


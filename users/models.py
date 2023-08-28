from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    
    email = models.EmailField(unique=True)
    profilePicture = models.ImageField(default='default/defaultpicture.jpg', upload_to='profileImages')

    def __str__(self):
        return self.email




# Generated by Django 4.2.4 on 2023-09-05 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_myfilemanager_totalfiledownload'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myfilemanager',
            name='totalFileDownload',
        ),
    ]
# Generated by Django 4.2.4 on 2023-09-05 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myfilemanager',
            name='downloadCount',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='myfilemanager',
            name='emailCount',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
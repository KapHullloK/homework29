# Generated by Django 4.2.2 on 2023-06-07 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='location',
            name='lng',
        ),
    ]

# Generated by Django 4.2.2 on 2023-06-13 10:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ads", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ads",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="pictures/"),
        ),
    ]

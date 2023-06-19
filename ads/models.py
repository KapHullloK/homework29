from users.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=60)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class ADS(models.Model):
    STATUS_CHOICES = [
        (True, 'Опубликовано'),
        (False, 'Не опубликовано')
    ]
    name = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    description = models.TextField(max_length=1000, null=True)
    is_published = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="pictures/", null=True, blank=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name

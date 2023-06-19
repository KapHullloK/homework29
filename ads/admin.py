from django.contrib import admin

from .models import Category, ADS

admin.site.register(ADS)
admin.site.register(Category)
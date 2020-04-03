from django.contrib import admin

# Register your models here.
from book import models

admin.site.register(models.BookCategories)
admin.site.register(models.BookDetail)
admin.site.register(models.Transaction)
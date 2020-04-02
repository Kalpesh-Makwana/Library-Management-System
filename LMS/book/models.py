from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class BookCategories(models.Model):
    
    name        = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.name

class BookDetail(models.Model):
    
    title       = models.CharField(max_length=64)
    author      = models.CharField(max_length=64)
    quantity    = models.PositiveIntegerField()
    category    = models.ForeignKey(BookCategories,on_delete=models.CASCADE)


    def __str__(self):
        return self.title



from django.db import models
from account.models import User
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

class Transaction(models.Model):
    ''' Books Transaction who issue book,which book are issue,how many time he/she ready the book '''

    STATUS = ((0,'Pending'),(1,'Issue'),(2,'Return'))
    
    book         = models.ForeignKey(BookDetail,on_delete=models.CASCADE)
    issue_by     = models.ForeignKey(User,on_delete=models.CASCADE)
    request_date = models.DateTimeField(default=timezone.now)
    issue_date   = models.DateTimeField(null=True,blank=True)
    return_date  = models.DateTimeField(null=True,blank=True)
    status       = models.PositiveIntegerField(choices=STATUS,default=0)

    def __str__(self):
        return self.book.title



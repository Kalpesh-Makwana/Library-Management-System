from django.shortcuts import render
from django.views import View
from . import models
# Create your views here.
class DisplayBook(View):
    def get(self,request,*args,**kwargs):
        books = models.BookDetail.objects.all()
        return render(request,'book/displaybook.html',{'books':books})
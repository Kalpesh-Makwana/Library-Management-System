from django.shortcuts               import render
from django.views                   import View
from .                              import models
from django.views.generic           import ListView,UpdateView,CreateView,DeleteView
from django.urls                    import reverse_lazy
# Create your views here.
class DisplayBook(View):
    def get(self,request,*args,**kwargs):
        books = models.BookDetail.objects.all()
        return render(request,'book/displaybook.html',{'books':books})
    
# class IssueBook(View):

class Listbook(ListView):
    ''' List Book in Librarian '''
    model               = models.BookDetail
    context_object_name = 'books'
    template_name       = 'book/listbook.html'

class UpdateBook(UpdateView):
    model         = models.BookDetail
    fields        = ('title','author','quantity','category')
    success_url   = reverse_lazy('book:listbook')
    template_name = 'book/updatebook.html'
    pk_url_kwarg  = 'id'
    extra_context = {'view':'Update'}

class CreateBook(CreateView):
    ''' Create Book by Librarian '''
    model         = models.BookDetail
    fields        = ('title','author','quantity','category')
    success_url   = reverse_lazy('book:listbook')
    template_name = 'book/updatebook.html'
    extra_context = {'view':'Add'}

class DeleteBook(DeleteView):
    model         = models.BookDetail
    success_url   = reverse_lazy('book:listbook')
    template_name = 'book/deletebook.html'
    pk_url_kwarg  = 'id'

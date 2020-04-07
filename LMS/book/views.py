from django.shortcuts               import render,get_object_or_404,redirect
from django.views                   import View
from .                              import models
from django.views.generic           import ListView,UpdateView,CreateView,DeleteView
from django.urls                    import reverse_lazy
from django.http                    import JsonResponse
from django.utils                   import timezone
from django.db.models               import Count,Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# Create your views here.
@method_decorator(login_required,name='dispatch')
class DisplayBook(View):
    def get(self,request,*args,**kwargs):
        books = models.BookDetail.objects.all()
        return render(request,'book/displaybook.html',{'books':books})

@method_decorator(login_required,name='dispatch') 
class IssueBook(View):
    def get(self,request,*args, **kwargs):
        total_book = models.Transaction.objects.filter(issue_by=request.user,status=0).aggregate(count=Count('issue_by'))['count']
        if total_book<3:
            id = request.GET.get('id',None)
            if id:
                book = get_object_or_404(models.BookDetail,id=id)
                if models.Transaction.objects.filter(book=book,issue_by=request.user,status__in=[0,1]).count()>0:
                    return JsonResponse(status=200,data={'success':True,'msg':"You sent request already for this Book "})

                if book.quantity>0:
                    models.Transaction.objects.create(book=book,issue_by=request.user)
                    book.quantity-=1
                    book.save()
                    return JsonResponse(status=200,data={'success':True,'msg':"Request Sent For This Book,Book bring from library",'deduce':True})  
                else:
                    return JsonResponse(status=203,data={'success':"This Book Not Available,You are not able to issue try after some time!"})
            else:
                return JsonResponse(status=203,data={'success':"This book not found in Library..!"})
        else:
            return JsonResponse(status=203,data={'success':"You already  "+str(total_book)+" book request so you must return at least one"})


@method_decorator(login_required,name='dispatch')
class ShowIssueBook(ListView):
    model           =   models.Transaction
    template_name   =   'book/showissuebook.html'
    extra_context   =   {'title':'Issue Book'}

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.model.objects.filter(status__in=[0,1])
        else:
            return self.model.objects.filter(issue_by=self.request.user,status__in=[0,1])



#Librarian
@method_decorator(login_required,name='dispatch')
class PendingRequest(View):
    def get(self,request,*args,**kwargs):
        transaction=models.Transaction.objects.filter(status__in=[0,1]).order_by('status','request_date')
        return render(request,'book/requests.html',{'obj':transaction})

@method_decorator(login_required,name='dispatch')
class AcceptRequest(View):
    def get(self,request,*args, **kwargs):
        id  = kwargs['id']     
        models.Transaction.objects.filter(id=id).update(status=1,issue_date=timezone.now(),return_date=None)  
        return redirect('book:pendingrequest')

@method_decorator(login_required,name='dispatch')
class DeleteRequest(View):
    def get(self,request,*args, **kwargs):
        id  = kwargs['id']     
        try:
            transaction = get_object_or_404(models.Transaction,id=id)  
            if transaction.status==0:
                book = get_object_or_404(models.BookDetail,id=transaction.book.id)  
                id   = transaction.book.id
                transaction.delete()

        except Exception as e:
            print(e)
        if request.user.is_staff:
            return redirect('book:pendingrequest')
        return redirect('book:issuebook')


#Book CRUD
@method_decorator(login_required,name='dispatch')
class Listbook(ListView):
    ''' List Book in Librarian '''
    model               = models.BookDetail
    context_object_name = 'books'
    template_name       = 'book/listbook.html'

@method_decorator(login_required,name='dispatch')
class UpdateBook(UpdateView):
    model         = models.BookDetail
    fields        = ('title','author','quantity','category')
    success_url   = reverse_lazy('book:listbook')
    template_name = 'book/updatebook.html'
    pk_url_kwarg  = 'id'
    extra_context = {'view':'Update'}

@method_decorator(login_required,name='dispatch')
class CreateBook(CreateView):
    ''' Create Book by Librarian '''
    model         = models.BookDetail
    fields        = ('title','author','quantity','category')
    success_url   = reverse_lazy('book:listbook')
    template_name = 'book/updatebook.html'
    extra_context = {'view':'Add'}

@method_decorator(login_required,name='dispatch')
class DeleteBook(DeleteView):
    model         = models.BookDetail
    success_url   = reverse_lazy('book:listbook')
    template_name = 'book/deletebook.html'
    pk_url_kwarg  = 'id'

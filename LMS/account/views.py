from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
from account import forms
from django.contrib.auth import logout,login,authenticate
from django.shortcuts import redirect
from django.views import View

# Create your views here.

class Index(TemplateView):
    '''template for display when user come'''
    template_name="account/index.html"

class Login(View):
    '''Login the user then render profile page'''

    def get(self,request,*args, **kwargs):
        form  = forms.LoginForm()
        return render(request,'account/login.html',{'form':form})

    def post(self,request,*args, **kwargs):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            user = authenticate(email=email,password=password)
            if user:
                login(request,user)
                messages.success(request,'Login Successfull..!')
                return redirect('account:index')    
            else:
                messages.error(request,'Fill Valid Data..!')
                return render(request,'account/login.html',{'form':form})            
        else:
            form  = forms.LoginForm()
            messages.error(request,'Fill Valid Data..!')
            return render(request,'account/login.html',{'form':form})            


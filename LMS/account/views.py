from django.shortcuts import render
from django.views.generic import TemplateView,DetailView
from django.contrib import messages
from account import forms
from django.contrib.auth import logout,login,authenticate
from django.shortcuts import redirect
from django.views import View
from account import models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
@method_decorator(login_required,name='dispatch')
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
                messages.error(request,'Unauthenticated Username Or Password!')
                return render(request,'account/login.html',{'form':form})            
        else:
            form  = forms.LoginForm()
            messages.error(request,'Unauthenticated Username Or Password!')
            return render(request,'account/login.html',{'form':form})            

class Singup(View):
    def get(self,request,*args, **kwargs):
        form = forms.SingupForm()   
        return render(request,'account/signup.html',{'form':form})

    def post(self,request,*args, **kwargs):
        form = forms.SingupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request,'Register Successfull..!')
            return redirect('account:login')
        else:
            form = forms.SingupForm(request.POST)
            messages.error(request,'Data Is Not Propere !')
            return render(request,'account/signup.html',{'form':form})
    

class Logout(View):
    def get(self, request):
        """ Logout the user """
        if request.user.is_authenticated:
            messages.success(request, "Logout Success.!!")
            logout(request)
            return redirect("account:login")
        else:
            messages.error(request, "you must have to logged-in before perform action")
            return redirect("account:login")


@method_decorator(login_required,name='dispatch')
class ProfileView(DetailView):
    model=models.User
    template_name='account/profile.html'


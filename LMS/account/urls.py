from django.urls import path,include
from account import views

app_name = 'account'

urlpatterns = [
    path('',views.Index.as_view(),name='index'),
    path('login',views.Login.as_view(),name='login'),
    path('singup',views.Singup.as_view(),name='signup'),
    path('logout',views.Logout.as_view(),name='logout'),
    path('<int:pk>/profile',views.ProfileView.as_view(),name='profile'),
]
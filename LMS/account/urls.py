from django.urls import path,include
from account import views
urlpatterns = [
    path('',views.Index.as_view(),name='index')

]
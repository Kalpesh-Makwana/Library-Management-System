from django.urls import path,include
from book import views
from . import views
app_name = 'book'

urlpatterns = [
    path('displaybook',views.DisplayBook.as_view(),name='displaybook'),
]
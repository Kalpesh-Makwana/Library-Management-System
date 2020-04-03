from django.urls import path,include
from book import views
from . import views

app_name = 'book'

urlpatterns = [
    path('displaybook',views.DisplayBook.as_view(),name='displaybook'),
    # path('issuebook/<int:b_id>',views.IssueBook.as_view(),name='issuebook'),
    
    #Book CRUD
    path('listbook',views.Listbook.as_view(),name='listbook'),
    path('<int:id>/updatebook',views.UpdateBook.as_view(),name='updatebook'),
    path('addbook',views.CreateBook.as_view(),name='addbook'),
    path('<int:id>/deletebook',views.DeleteBook.as_view(),name='deletebook'),

]
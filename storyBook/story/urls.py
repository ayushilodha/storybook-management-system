from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('home/', views.home),
    path('display/', views.display),
    path('delete/', views.delete),
    path('modify/', views.modify),
    path('modify1/', views.modify1),
    path('add/', views.add),
    path('login/',views.login),
]
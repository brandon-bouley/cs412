from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),  # Add this line to map the root URL
    path('main/', views.main, name='main'),
    path('order/', views.order, name='order'),
    path('confirmation/', views.confirmation, name='confirmation'),
]
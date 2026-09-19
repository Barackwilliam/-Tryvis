from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('our-work/', views.our_work, name='our_work'),
    path('contact/', views.contact, name='contact'),
]

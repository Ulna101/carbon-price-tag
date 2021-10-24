from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('qr', views.qr, name='qr'),
    path('tag', views.tag, name='tag')
]
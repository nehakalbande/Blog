from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [

path('', views.contact, name='contact'),
path('signup/', views.handleSignup, name='handleSignup'),
path('login/', views.handleLogin, name='handleLogin'),
path('logout/', views.handleLogout, name='handleLogout'),


]
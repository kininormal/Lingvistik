from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('1/', views.index, name = "index"),
    path('2/', views.prevfollow, name = "prevfollow"),
    path('3/', views.treesentences, name = "treesentences"),
]
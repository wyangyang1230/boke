from django.contrib import admin
from django.urls import path,re_path
from Article.views import *

urlpatterns = [
    path('base/',base),
    path('index/',index),
    path('about/',about),
    path('listpic/', listpic),
    path('newslistpic/',newslistpic),
    re_path('newslistpic/(?P<page>\d+)',newslistpic),
    re_path('articledetails/(?P<id>\d+)',articledetails),
]
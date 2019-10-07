from django.urls import path,re_path
from Back.views import *

urlpatterns = [
    path('register/',register),
    path('login/',login),
    path('index/',index),
    path('logout/',logout),
    path('personal_info/', personal_info),
    path('add_article/',add_article),
    path('list_article/',list_article),
    path('get_article/',get_article),
    re_path('get_article/(?P<id>\d+)',get_article),
]
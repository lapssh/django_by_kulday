from django.urls import path

from news.views import index, test

urlpatterns = [
    path('', index),
    path('test/', test),
]
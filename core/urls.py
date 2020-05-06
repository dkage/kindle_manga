from django.urls import path
import core.views as core

urlpatterns = [
    path('', core.index, name='index'),
    path('index', core.index),

    path('register', core.register, name='register')
]
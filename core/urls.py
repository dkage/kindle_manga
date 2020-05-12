from django.urls import path
import core.views as core

urlpatterns = [
    path('', core.index, name='index'),
    path('index', core.index),

    path('register', core.register, name='register'),
    path('account_success', core.account_success, name='account_success'),
    path('login', core.login, name='login'),
    path('test', core.test, name='test'),

]
from django.urls import path

import core.views as core

urlpatterns = [
    # Initial paths
    path('', core.index, name='index'),
    path('index', core.index),

    # Auth paths
    path('signin', core.signin, name='signin'),
    path('signup', core.signup, name='signup'),
    path('account_success', core.account_success, name='account_success'),
    path('test', core.test, name='test'),

    # App paths
    path('dashboard', core.dashboard, name='home'),
]

from django.urls import path

import core.views as core

urlpatterns = [
    # Initial paths
    path('', core.index, name='index'),
    path('index', core.index),

    # Auth paths
    path('signin', core.signin, name='signin'),
    path('signup', core.signup, name='signup'),
    path('signout', core.signout, name='signout'),
    path('account', core.account, name='account'),
    path('account_success', core.account_success, name='account_success'), # TODO delete this?
    path('test', core.test, name='test'),

    # App paths
    path('dashboard', core.index, name='home'),
    path('admin', core.admin_menu, name='admin'),
]

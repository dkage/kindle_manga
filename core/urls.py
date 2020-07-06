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

    # App paths
    path('dashboard', core.index, name='home'),
    path('restricted', core.restricted, name='restricted'),

    # Routine calls paths
    path('full_scan', core.full_scan, name='full_scan')
]

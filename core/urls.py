from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import core.views as core

urlpatterns = [
    # Initial paths
    path('', core.index, name='index'),
    path('index', core.index),
    path('about', core.about, name='about'),

    # Auth paths
    path('signin', core.signin, name='signin'),
    path('signup', core.signup, name='signup'),
    path('signout', core.signout, name='signout'),
    path('account', core.account, name='account'),
    path('account_success', core.account_success, name='account_success'),  # TODO delete this?

    # App paths
    path('dashboard', core.index, name='home'),
    path('restricted', core.restricted, name='restricted'),
    path('manga_list', core.MangaListView.as_view(), name='manga_list'),
    path('manga/<int:pk>', core.MangaDetailView.as_view(), name='manga'),
    path('test/<int:pk>', core.test, name='test'),

    # AJAX CRUDs paths
    path('full_scan', core.full_scan, name='full_scan'),
    path('subscribe', core.subscribe, name='subscribe'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Adds /media/ folder to urls

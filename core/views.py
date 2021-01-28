# Django
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from defines import COVERS_DIR
from django.core.exceptions import ObjectDoesNotExist
# App
from core.forms import SignUpForm, SignInForm
from core.models import SystemLog, Manga, Chapter
# Scraper
from functions.spider import get_all_series, get_all_chapters, get_image_url, BASE_URL, check_cover
# Log functions
from core.log_functions import log_basic_entry, log_full_scan_query
# Misc
from datetime import datetime
import os
import re


def index(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=1)
        subscriptions = user.subscriptions.all()

        covers = dict()
        for sub in subscriptions:
            # TODO add function to check if cover image is already downloaded here
            series_url = sub.manga_reader_url
            img_name = ''.join([series_url.replace('/', ''), '.jpg'])
            covers[sub.id] = img_name

        db_data = {'subs': subscriptions,
                   'covers': covers,
                   'base_url': BASE_URL}

        return render(request, 'dashboard.html', context=db_data)
    else:
        return render(request, 'index.html')


@login_required(login_url='signin')
def restricted(request):
    """
    Loads restricted page if user is Super User only.

    :param request: Django request object
    :return: return view for restricted webpage, or redirects to basic index.
    """

    if request.user.is_superuser:
        system_log = log_full_scan_query()
        return render(request, 'restricted.html', {'system_log': system_log})
    else:
        return redirect('index')


@login_required(login_url='signin')
def dashboard(request):
    return redirect('index')


def signup(request):

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('account_success')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'user_form': form})


def signout(request):
    logout(request)

    return render(request, 'index.html')


def account_success(request):
    return render(request, 'account_success.html')


def signin(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':

        form = SignInForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'signin_form': form})


@login_required(login_url='signin')
def account(request):
    return render(request, 'account.html')


class MangaListView(LoginRequiredMixin, ListView):
    login_url = '/signin'
    redirect_field_name = '/manga_list'

    model = Manga
    template_name = 'manga_list.html'
    ordering = ['series_name']


class MangaDetailView(LoginRequiredMixin, DetailView):
    login_url = '/signin'
    redirect_field_name = '/manga_list'

    model = Manga
    template_name = 'manga.html'

    # Grabs additional data, not included in the DetailView generic view.
    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context for the current object being detailed
        context = super().get_context_data(**kwargs)

        # Check if user is subbed already to current manga
        user = User.objects.get(id=self.request.user.id)
        sub_list = Manga.objects.get(id=self.object.id).subscribers.all()
        if user in sub_list:
            context['subbed'] = True
        else:
            context['subbed'] = False

        # Grabs manga cover image
        series_url = self.object.manga_reader_url
        self.object.cover = check_cover(series_url)

        # Grabs every chapter for given manga
        try:
            context['chapters'] = Chapter.objects.filter(manga_id=self.object.id).order_by('id')
        except Chapter.DoesNotExist:
            context['chapters'] = None

        return context


def about(request):
    return render(request, 'about.html')


def full_scan(request):
    """
    Makes the full scan on mangareader, checking for every manga available in their catalogue, and adding to database.
    Creates a log with the SuperUser that triggered the full_scan call, scraps all titles and then insert on database
    if not already exists.

    :param request: Django request object
    :return:
    """

    log_basic_entry(request, 'Full Scan started')

    all_series_array = get_all_series()
    for series in all_series_array:
        try:
            Manga.objects.get(series_name=series[0], manga_reader_url=series[1])
        except Manga.DoesNotExist:
            manga = Manga(series_name=series[0], manga_reader_url=series[1])
            manga.save()

    log_basic_entry(request, 'Full Scan finished successfully')

    return HttpResponse('Full scan executed.')


@login_required(login_url='signin')
def chapter_scan(request):
    """
    This function checks every chapter available for the manga with ID received as parameter.

    :param request: Django request object;
    :return:
    """

    manga_model = get_object_or_404(Manga, pk=request.POST['manga_id'])  # Query for grabbing the ID Manga info.
    chapters = get_all_chapters(manga_model.manga_reader_url)  # Grabs all chapters from mangareader using the URL

    log_message = 'Chapter Scan started - ' + manga_model.series_name
    log_basic_entry(request, log_message)

    # Saves every chapter not yet on the database.
    for chapter in chapters:
        chapter_model = Chapter(chapter=chapter[0],
                                chapter_title=chapter[1],
                                chapter_url=chapter[2],
                                chapter_date=datetime.strptime(chapter[3], '%m/%d/%Y').date(),
                                manga_id=manga_model.id)
        if not Chapter.objects.filter(chapter=chapter[0], manga_id=request.POST['manga_id']).exists():
            chapter_model.save()

    # TODO improve error handling to add to log
    log_message = 'Chapter Scan finished - ' + manga_model.series_name
    log_basic_entry(request, log_message)

    # TODO improve return with response for AJAX call
    return HttpResponse('test')


def subscribe(request):

    user = User.objects.get(id=request.user.id)
    manga = Manga.objects.get(id=request.POST['manga_id'])

    if user in manga.subscribers.all():
        user.subscriptions.remove(manga)
    else:
        user.subscriptions.add(manga)
    user.save()

    return HttpResponse('ok')

# Django
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from defines import COVERS_DIR
# App
from core.forms import SignUpForm, SignInForm
from core.models import SystemLog, Manga, Chapter
# Scraper
from functions.spider import get_all_series, get_all_chapters, get_image_url, BASE_URL, download_cover
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
    if request.user.is_superuser:

        try:
            system_log = SystemLog.objects.filter(operation='Full Scan').order_by('-date')[0]
        except IndexError:
            system_log = dict()
            system_log['triggered_by'] = 'Not done yet'
            system_log['date'] = ''

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

        series_url = self.object.manga_reader_url

        img_name = ''.join([series_url.replace('/', ''), '.jpg'])
        cover_path = os.path.join(COVERS_DIR, img_name)

        self.object.cover = img_name
        # Check if cover is already downloaded, if it isn't, scrap and download from mangareader
        if not os.path.isfile(cover_path):
            download_cover(series_url)

        return context


def about(request):
    return render(request, 'about.html')


def test(request, pk):
    # death note = 1074
    manga_model = get_object_or_404(Manga, pk=2778)

    chapters = get_all_chapters(manga_model.manga_reader_url)  # Grabs all chapters from manga_reader URL

    for chapter in chapters:
        chapter_model = Chapter(chapter=chapter[0],
                                chapter_title=chapter[1],
                                chapter_url=chapter[2],
                                chapter_date=datetime.strptime(chapter[3], '%m/%d/%Y').date(),
                                manga_id=manga_model.id)
        if not Chapter.objects.filter(chapter=chapter[0], manga_id=pk).exists():
            chapter_model.save()

    # when relationship entry is not found yet
    # try:
    #     print(manga_model.chapter)
    # except ObjectDoesNotExist:
    #     return HttpResponse('faiou')

    return HttpResponse('test')


def full_scan(request):

    logger = SystemLog()
    logger.operation = 'Full Scan'
    user = User.objects.get(id=request.user.id)
    logger.triggered_by = user
    logger.save()

    all_series_array = get_all_series()

    for series in all_series_array:
        try:
            Manga.objects.get(series_name=series[0], manga_reader_url=series[1])
        except Manga.DoesNotExist:
            manga = Manga(series_name=series[0], manga_reader_url=series[1])
            manga.save()

    # TODO add another log, and find a way to return when finished in ajax

    return HttpResponse('Full scan executed.')


def subscribe(request):

    user = User.objects.get(id=request.user.id)
    manga = Manga.objects.get(id=request.POST['manga_id'])

    if user in manga.subscribers.all():
        user.subscriptions.remove(manga)
    else:
        user.subscriptions.add(manga)
    user.save()

    return HttpResponse('ok')

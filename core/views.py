from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView
# App
from core.forms import SignUpForm, SignInForm
from core.models import SystemLog, Manga
# Scraper
from functions.spider import get_all_series, get_image_url, BASE_URL


def index(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=1)
        subscriptions = user.subscriptions.all()

        covers = dict()
        for sub in subscriptions:
            covers[sub.id] = get_image_url(sub.manga_reader_url)

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


def full_scan(request):

    logger = SystemLog()
    logger.operation = 'Full Scan'
    logger.triggered_by = request.user.username
    logger.triggered_by_id = request.user.id
    logger.save()

    all_series_array = get_all_series()

    for series in all_series_array:
        try:
            Manga.objects.get(series_name=series[0], manga_reader_url=series[1])
        except Manga.DoesNotExist:
            manga = Manga(series_name=series[0], manga_reader_url=series[1])
            manga.save()

    # TODO add another log, and find a way to return when finished in ajax

    return HttpResponse('Adrian, I did it')


class MangaListView(LoginRequiredMixin, ListView):
    login_url = '/signin'
    redirect_field_name = '/manga_list'

    model = Manga
    template_name = 'manga_list.html'
    ordering = ['series_name']


def about(request):
    return render(request, 'about.html')

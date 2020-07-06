from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# App
from core.forms import SignUpForm, SignInForm
from core.models import SystemLog, Manga
# Scraper
from functions.spider import get_all_series

def index(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    else:
        return render(request, 'index.html')


@login_required(login_url='signin')
def restricted(request):
    if request.user.is_superuser:
        system_log = SystemLog.objects.filter(operation='Full Scan').order_by('-date')[0]

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
        print(form)
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
        print(request.POST)
        form = SignInForm(data=request.POST)
        print(form)
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
    # all_series = get_all_series()
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

    return HttpResponse('Adrian, I did it')

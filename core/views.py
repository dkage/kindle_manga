from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from core.forms import SignUpForm, SignInForm


def index(request):
    return render(request, 'index.html')


@login_required(login_url='signin')
def dashboard(request):
    return render(request, 'dashboard_old.html')


def signup(request):

    if request.user.is_authenticated:
        return render(request, 'dashboard_old.html')

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
    return render(request, 'account_success_old.html')


def signin(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')

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


def test(request):
    return render(request, 'test.html')

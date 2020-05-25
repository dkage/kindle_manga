from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from core.forms import SignUpForm


def index(request):
    return render(request, 'index.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def signup(request):
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


def account_success(request):
    return render(request, 'account_success.html')


def signin(request):
    return render(request, 'login.html')


def test(request):
    return render(request, 'test.html')
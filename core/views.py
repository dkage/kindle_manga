from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from core.forms import SignUpForm, SignInForm


def index(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    else:
        return render(request, 'index.html')


@login_required(login_url='signin')
def admin_menu(request):
    if request.user.is_superadmin:
        return render(request, 'admin.html')
    else:
        return render(request, 'dashboard.html')


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


def account(request):
    return render(request, 'account.html')




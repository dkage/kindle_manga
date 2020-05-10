from django.shortcuts import render, redirect
from .forms import UserProfileForm
from secrets import compare_digest


def index(request):
    return render(request, 'index.html')


def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST)

        if user_form.is_valid():
            if not compare_digest(user_form.password, user_form.password_confirm):
                raise user_form.ValidationError('Your passwords do not match', code='invalid')
            else:
                user = user_form.save()
                user.set_password(user.password)
                user.save()

                return redirect('account_created')
    else:
        user_form = UserProfileForm()

    return render(request, 'register.html', {'user_form': user_form})


def login(request):
    return render(request, 'login.html')


def test(request):
    return render(request, 'test.html')
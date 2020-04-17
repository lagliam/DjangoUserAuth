from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash # for password updates
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import SignUpForm, EditProfileForm


def home(request):
    return render(request, 'userauth/home.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Succeeded')
            return redirect('home')
        else:
            messages.success(request, 'Login Failed')
            return redirect('login')
    return render(request, 'userauth/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'Logout succeeded')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration Succeeded')
            return redirect('home')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'userauth/register.html', context)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Edit Succeeded')
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)
    context = {'form': form}
    return render(request, 'userauth/edit_profile.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Change Password Succeeded')
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)
    context = {'form': form}
    return render(request, 'userauth/change_password.html', context)

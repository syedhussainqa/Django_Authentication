from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .forms import SignUpForm, EditProfileForm

def home(request):
    return render(request, 'authenticate/home.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have successfully logged in!'))
            return redirect('home')
        else:
            messages.success(request, ('Error logging in, please log in again...!'))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request,'You have been logged out...')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        # creating a register form
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            user = authenticate(request, username=username, password=password)
            # user registers top 3 lines, user is auto logged in when register bottom
            login(request, user)
            messages.success(request, 'You have been registered...')
            return redirect('home')
    else:
        # no param because nothing is passed
        form = SignUpForm()

    context = {
       'form': form,
    }
    return render(request, 'authenticate/register.html', context)

def edit_profile(request):
    if request.method == 'POST':
        # Editing user profile, instance=request.user to pass in users info to the form
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated...')
            return redirect('home')
    else:
        # no param because nothing is passed
        form = EditProfileForm(instance=request.user)

    context = {
       'form': form,
    }
    return render(request, 'authenticate/edit_profile.html', context)

def change_password(request):
    if request.method == 'POST':
        # Editing user profile, instance=request.user to pass in users info to the form
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password updated...')
            return redirect('home')
    else:
        # no param because nothing is passed
        form = PasswordChangeForm(user=request.user)

    context = {
       'form': form,
    }
    return render(request, 'authenticate/change_password.html', context)


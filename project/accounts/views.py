from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegisterForm, UserLoginForm, ChangePasswordForm
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy


# S'enregistrer
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


# Login
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts:admin_index')
            else:
                print("Authentication failed: user is None")
        else:
            print("Form is not valid")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


# Logout
@login_required
def user_logout(request):
    logout(request)
    return redirect('main:index')


# Account detail
@login_required
def my_account(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'accounts/my_account.html', context)


### ADMIN ###
# Admin redirect
@login_required
def admin_redirect(request):
    return redirect('accounts:admin_index')


# Admin redirect
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_index(request):
    return render(request, 'accounts/admin/index.html')


# Change password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data['old_password']):
                if form.cleaned_data['new_password'] == form.cleaned_data['confirm_password']:
                    user.set_password(form.cleaned_data['new_password'])
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Votre mot de passe a été changé avec succès.')
                    if not user.is_superuser:
                        return redirect(reverse_lazy('accounts:my_account'))
                    else:
                        return redirect(reverse_lazy('accounts:admin_index'))
                else:
                    messages.error(request, 'Les nouveaux mots de passe ne correspondent pas.')
            else:
                messages.error(request, 'L\'ancien mot de passe est incorrect.')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = ChangePasswordForm()
    return render(request, 'accounts/password_reset/change_password.html', {'form': form})
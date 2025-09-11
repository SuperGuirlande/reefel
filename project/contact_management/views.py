from django.shortcuts import render, redirect
from .forms import ContactInfosForm, ChangeUserNamesForm, ChangeUserEmailForm
from .models import ContactInfos
from django.contrib import messages


def change_contact_infos(request):
    contact_infos = ContactInfos.objects.first()

    if request.method == 'POST':
        form = ContactInfosForm(request.POST, instance=contact_infos)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informations de contact mises à jour avec succès.')
            return redirect('accounts:admin_index')
    else:
        form = ContactInfosForm(instance=contact_infos)

    context = {
        'form': form,
    }

    return render(request, 'contact_management/change_contact_infos.html', context)


def change_user_names_form(request):
    user = request.user

    if request.method == 'POST':
        form = ChangeUserNamesForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informations de compte mises à jour avec succès.')
            return redirect('accounts:admin_index')
    else:
        form = ChangeUserNamesForm(instance=user)

    context = {
        'form': form,
    }

    return render(request, 'contact_management/change_user_names_form.html', context)


def change_user_email_form(request):
    user = request.user

    if request.method == 'POST':
        form = ChangeUserEmailForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Email de connexion mise à jour avec succès.')
            return redirect('accounts:admin_index')
        else:
            messages.error(request, 'Email de connexion invalide.')
    else:
        form = ChangeUserEmailForm(instance=user)

    context = {
        'form': form,
    }

    return render(request, 'contact_management/change_user_email_form.html', context)

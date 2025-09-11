from django.shortcuts import render, redirect
from contact_management.forms import ContactForm
from django.contrib import messages


def index(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'main/index.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre message à été envoyé avec succès')
            messages.success(request, 'Vous serez contactez d\'ici 48 heures')
            return redirect('main:contact')
        else:
            messages.error(request, 'Veuillez vérifier les informations du formulaire')
    else:
        form = ContactForm()

    user = request.user
    context = {
        'user': user,
        'form': form,
    }
    return render(request, 'main/contact.html', context)

from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse

def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'autores/register_view.html', {
        'form': form,
        'form_action': reverse('autores:create'),
    })

def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        usuario = form.save(commit=False)
        usuario.set_password(usuario.password)
        usuario.save()
        messages.success(request, 'Seu usuário foi criado, por favor, faça o login')
        del(request.session['register_form_data'])

    return redirect('autores:register')

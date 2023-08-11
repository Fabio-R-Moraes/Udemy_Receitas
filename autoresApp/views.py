from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import Http404

def register_view(request):
    request.session['numero'] = request.session.get('numero') or 1
    request.session['numero'] += 1
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'autores/register_view.html', {
        'form': form,
    })

def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    return redirect('autores:register')

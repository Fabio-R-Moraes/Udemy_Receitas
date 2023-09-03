from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'autores/register_view.html', {
        'form': form,
        'form_action': reverse('autores:register_create'),
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
        return redirect(reverse('autores:login'))

    return redirect('autores:register')

def login_view(request):
    form = LoginForm()
    return render(request, 'autores/login.html', {
        'form': form,
        'form_action': reverse('autores:login_create')
    })

def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    login_url = reverse('autores:login')

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', '')
        )

        if authenticated_user is not None:
            messages.success(request, 'Você está logado!!!')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Credenciais inválidas...')
    else:
        messages.error(request, 'Usuário ou Senha inválidos!!!')

    return redirect(login_url)

@login_required(login_url='autores:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Solicitação de logout inválida!')
        return redirect(reverse('autores:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Você está tentando sair com OUTRO usuário!!!')
        return redirect(reverse('autores:login'))

    messages.success(request, 'Usuário deslogado com sucesso!!!')
    logout(request)
    return redirect(reverse('autores:login'))

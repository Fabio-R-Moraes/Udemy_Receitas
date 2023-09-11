from django.shortcuts import render, redirect
from autoresApp.forms import LoginForm, RegisterForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from receitasApp.models import Receitas
from autoresApp.forms.receita_form import AutoresReceitaForm

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

    return redirect(reverse('autores:dashboard'))

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

@login_required(login_url='autores:login', redirect_field_name='next')
def dashboard(request):
    minhas_receitas = Receitas.objects.filter(
        esta_publicado=False,
        autor=request.user
    )
    return render(
        request,
        'autores/dashboard.html',
        context={
                'receitas': minhas_receitas,
        }
    )

@login_required(login_url='autores:login', redirect_field_name='next')
def dashboard_receita_edit(request, id):
    minha_receita = Receitas.objects.filter(
        esta_publicado=False,
        autor=request.user,
        pk=id,
    ).first()

    if not minha_receita:
        raise Http404()

    formulario = AutoresReceitaForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance= minha_receita
    )

    if formulario.is_valid():
        #Agora o formulário é válido e u posso tentar salvar
        receita = formulario.save(commit=False)
        receita.autor = request.user
        receita.modo_preparo_html = False
        receita.esta_publicado = False

        receita.save()
        messages.success(request, 'Sua receita foi salva com sucesso!!!')
        return redirect(reverse('autores:dashboard_receita_edit', args=(id,)))

    return render(
        request,
        'autores/dashboard_receitas.html',
        context={
            'form': formulario
        }
    )

@login_required(login_url='autores:login', redirect_field_name='next')
def dashboard_receita_nova(request):
    formulario = AutoresReceitaForm(
        data=request.POST or None,
        files=request.FILES or None
    )

    if formulario.is_valid():
        #Agora o formulário é válido e eu posso tentar salvar
        receita: Receitas = formulario.save(commit=False)
        receita.autor = request.user
        receita.modo_preparo_html = False
        receita.esta_publicado = False

        receita.save()
        messages.success(request, 'Sua receita foi salva com sucesso!!!')
        return redirect(reverse('autores:dashboard_receita_edit', args=(receita.id,)))

    return render(
        request,
        'autores/dashboard_receitas.html',
        context={
            'form': formulario,
            'form_action': reverse('autores:dashboard_receita_nova')
        }
    )

@login_required(login_url='autores:login', redirect_field_name='next')
def dashboard_receita_delete(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    id = POST.get('id')

    minha_receita = Receitas.objects.filter(
        esta_publicado=False,
        autor=request.user,
        pk=id,
    ).first()

    if not minha_receita:
        raise Http404()

    minha_receita.delete()
    messages.success(request, 'Receita excluída com sucesso!!!!')

    return redirect(reverse('autores:dashboard'))

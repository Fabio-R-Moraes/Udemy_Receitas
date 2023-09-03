from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Receitas
from django.http import Http404
from django.db.models import Q
from utils.paginacao import make_pagination
import os
from django.contrib import messages

POR_PAGINA = os.environ.get('RECEITAS_POR_PAGINA', 6)

def home(request):
    # receitas = Receitas.objects.filter(esta_publicado=True).order_by('-id')
    receitas = Receitas.objects.filter(
        esta_publicado=True,
        ).order_by('-id')

    pagina_objeto, range_paginacao = make_pagination(request, receitas, POR_PAGINA)

    '''
    messages.success(
        request, 'Oiiii... você ganhou uma mensagem de sucesso!!!')

    messages.error(
        request, 'Oiiii... você tomou um erro!!!')

    messages.info(
        request, 'Oiiii... essa mensagem é apenas informativa!!!')
    '''

    return render(request, 'receitas/home.html', context={
        'receitas': pagina_objeto,
        'range_paginacao': range_paginacao,
        })
    # HTTP Response

def categoria(request, categoria_id):
    receitas = get_list_or_404(Receitas.objects.filter(
        categoria__id=categoria_id,
        esta_publicado=True,
        ).order_by('-id'))

    pagina_objeto, range_paginacao = make_pagination(request, receitas, POR_PAGINA)

    return render(request, 'receitas/categoria.html', context={
        'receitas': pagina_objeto,
        'range_paginacao': range_paginacao,
        'titulo': f'{receitas[0].categoria.nome} - Categoria | '
        })
    # HTTP Response

def receita(request, id):
    # receita = Receitas.objects.filter(
    #        pk=id,
    #        esta_publicado=True,
    #        ).order_by('-id').first()

    receita = get_object_or_404(Receitas, pk=id, esta_publicado=True)

    return render(request, 'receitas/receita-view.html', context={
        'receita': receita,
        'is_detail_page': True,
    })
    # HTTP Request

def pesquisa(request):
    messages.success(request, 'Oiiii... você veio pesquisar algo... eu viiii!!!')
    termo_procurado = request.GET.get('q', '').strip()

    if not termo_procurado:
        raise Http404()

    receitas = Receitas.objects.filter(
        Q(
        Q(titulo__icontains=termo_procurado) |
        Q(descricao__icontains=termo_procurado),
        ),
        esta_publicado=True,
        ).order_by('-titulo')

    pagina_objeto, range_paginacao = make_pagination(request, receitas, POR_PAGINA)

    return render(request, 'receitas/pesquisa.html', {
        'page_title': f'Pesquisando por "{termo_procurado}" |',
        'receitas': pagina_objeto,
        'range_paginacao': range_paginacao,
        'adicional_url_query': f'&q={termo_procurado}',
        })

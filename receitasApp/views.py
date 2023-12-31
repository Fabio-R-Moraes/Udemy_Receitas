from .models import Receitas
from django.http.response import Http404
from utils.paginacao import make_pagination
import os
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.aggregates import Count
from tagApp.models import Tag
from django.utils import translation
from django.utils.translation import gettext as _

POR_PAGINA = os.environ.get('RECEITAS_POR_PAGINA', 6)

def teoria(request, *args, **kwargs):
    #Pegando um elemento através de objects.get
    #try:
    #    receitas = Receitas.objects.get(pk=4)
    #except ObjectDoesNotExist:
     #   receitas = None

    #receitas = Receitas.objects.all()

    #Vem uma lista ordenada
    #receitas = receitas.filter(titulo__icontains='Arroz')
    #Vem o primeiro item
    #receitas = receitas.filter(titulo__icontains='Arroz').order_by('-id').first()
    #Vem o último item
    #receitas = receitas.filter(titulo__icontains='Arroz').order_by('-id').last()

    #print(receitas[0].titulo)

    #Pegando as receitas com ID IGUAL ao do USUÁRIO
    #receitas = Receitas.objects.filter(
    #    id=F('autor__id')
    #)[0:10]
    #receitas = receitas.select_related('autor')

    receitas = Receitas.objects.get_publicados()
    numero_de_receitas = receitas.aggregate(total=Count('id'))

    contexto = {
        'receitas': receitas,
        'total_receitas': numero_de_receitas['total']
    }
    return render(
        request,
        'receitas/teoria.html',
        context=contexto
    )

class ReceitaListViewBase(ListView):
    model = Receitas
    paginate_by = None
    context_object_name = 'receitas'
    ordering = ['-id']
    template_name = 'receitas/home.html'

    def get_queryset(self, *args, **kwargs):
        consulta = super().get_queryset(*args, **kwargs)
        consulta = consulta.filter(
            esta_publicado=True,
        )
        consulta = consulta.select_related('autor', 'categoria')
        consulta = consulta.prefetch_related('tags', 'autor__profile')

        return consulta

    def get_context_data(self, *args, **kwargs):
        contexto = super().get_context_data(*args, **kwargs)
        pagina_objeto, range_paginacao = make_pagination(
            self.request,
            contexto.get('receitas'),
            POR_PAGINA
        )
        html_language = translation.get_language()
        contexto.update(
            {
                'receitas': pagina_objeto,
                'range_paginacao': range_paginacao,
                'html_language': html_language,
            }
        )

        return contexto

class ReceitaListViewHome(ReceitaListViewBase):
    template_name = 'receitas/home.html'

class ReceitaListViewHomeAPI(ReceitaListViewBase):
    template_name = 'receitas/home.html'

    def render_to_response(self, context, **response_kwargs):
        receitas = self.get_context_data()['receitas']
        receitas_lista = receitas.object_list.values()

        #print(receitas_lista)

        return JsonResponse(
            list(receitas_lista),
            safe=False,
        )

class ReceitaListViewCategoria(ReceitaListViewBase):
    template_name = 'receitas/categoria.html'

    def get_context_data(self, *args, **kwargs):
        contexto = super().get_context_data(*args, **kwargs)
        category_translation = _('Category')

        contexto.update({
            'titulo': f'{contexto.get("receitas")[0].categoria.nome} - {category_translation} | '
        })

        return contexto

    def get_queryset(self, *args, **kwargs):
        consulta = super().get_queryset(*args, **kwargs)
        consulta = consulta.filter(
            esta_publicado=True,
            categoria__id= self.kwargs.get('categoria_id')
        )

        if not consulta:
            raise Http404()

        return consulta

class ReceitaListViewPesquisa(ReceitaListViewBase):
    template_name = 'receitas/pesquisa.html'

    def get_context_data(self, *args, **kwargs):
        contexto = super().get_context_data(*args, **kwargs)
        termo_procurado = self.request.GET.get('q', '').strip()

        if not termo_procurado:
            raise Http404()

        contexto.update({
            'page_title': f'Pesquisando por "{termo_procurado}" |',
            'termo_procurado': termo_procurado,
            'adicional_url_query': f'&q={termo_procurado}',
        })

        return contexto

    def get_queryset(self, *args, **kwargs):
        termo_procurado = self.request.GET.get('q', '').strip()
        consulta = super().get_queryset(*args, **kwargs)
        consulta = consulta.filter(
            Q(
                Q(titulo__icontains=termo_procurado) |
                Q(descricao__icontains=termo_procurado),
            ),
            esta_publicado=True,
        )

        return consulta

class ReceitaDetail(DetailView):
    model = Receitas
    context_object_name = 'receita'
    template_name = 'receitas/receita-view.html'

    def get_queryset(self, *args, **kwargs):
        consulta = super().get_queryset(*args, **kwargs)
        consulta = consulta.filter(esta_publicado=True,)

        return consulta

    def get_context_data(self, *args, **kwargs):
        contexto = super().get_context_data(*args, **kwargs)
        contexto.update({
            'is_detail_page': True,
        })

        return contexto

class ReceitaDetailAPI(ReceitaDetail):
    def render_to_response(self, context, **response_kwargs):
        receita = self.get_context_data()['receita']
        receita_dicionario = model_to_dict(receita)

        receita_dicionario['criado_em'] = str(receita.criado_em)
        receita_dicionario['atualizado_em'] = str(receita.atualizado_em)

        if receita_dicionario.get('receita_imagem'):
            receita_dicionario['receita_imagem'] = self.request.build_absolute_uri() + \
                            receita_dicionario['receita_imagem'].url
        else:
            receita_dicionario['receita_imagem'] = ''

        del receita_dicionario['esta_publicado']
        del receita_dicionario['modo_preparo_html']

        return JsonResponse(
            receita_dicionario,
            safe=False,
        )

class ReceitaListViewTag(ReceitaListViewBase):
    template_name = 'receitas/tag.html'

    def get_context_data(self, *args, **kwargs):
        contexto = super().get_context_data(*args, **kwargs)
        titulo_pagina = Tag.objects.filter(slug=self.kwargs.get('slug', '')).first()

        if not titulo_pagina:
             titulo_pagina = 'Sem receitas para mostrar...'

        titulo_pagina = f'{titulo_pagina.nome} - Tag |'

        contexto.update({
            'titulo_pagina': titulo_pagina,
        })

        return contexto

    def get_queryset(self, *args, **kwargs):
        consulta = super().get_queryset(*args, **kwargs)
        consulta = consulta.filter(tags__slug=self.kwargs.get('slug', ''))

        return consulta

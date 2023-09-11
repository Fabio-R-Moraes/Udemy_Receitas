from django.views import View
from receitasApp.models import Receitas
from django.http import Http404
from autoresApp.forms.receita_form import AutoresReceitaForm
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

class DashboardReceitas(View):
    def get(self, request, id):
        print('ESTOU USANDO CLASS BASED VIEWS...')
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
            instance=minha_receita
        )

        if formulario.is_valid():
            # Agora o formulário é válido e u posso tentar salvar
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

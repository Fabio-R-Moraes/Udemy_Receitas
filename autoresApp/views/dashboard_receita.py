from django.views import View
from receitasApp.models import Receitas
from django.http import Http404
from autoresApp.forms.receita_form import AutoresReceitaForm
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(
    login_required(login_url='autores:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardReceitas(View):
    def get_receita(self, id=None):
        minha_receita = None

        if id is not None:
            minha_receita = Receitas.objects.filter(
                esta_publicado=False,
                autor=self.request.user,
                pk=id,
            ).first()

            if not minha_receita:
                raise Http404()

        return minha_receita

    def render_receita(self, formulario):
        return render(
            self.request,
            'autores/dashboard_receitas.html',
            context={
                'form': formulario
            }
        )

    def get(self, request, id=None):
        #print('ESTOU USANDO CLASS BASED VIEWS...')
        minha_receita = self.get_receita(id)
        formulario = AutoresReceitaForm(instance=minha_receita)

        return self.render_receita(formulario)

    def post(self, request, id=None):
        minha_receita = self.get_receita(id)

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
            return redirect(reverse('autores:dashboard_receita_edit', args=(
                receita.id,
            )))

        return self.render_receita(formulario)

@method_decorator(
    login_required(login_url='autores:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardReceitaDelete(DashboardReceitas):
    def post(self, *args, **kwargs):
        minha_receita = self.get_receita(self.request.POST.get('id'))

        minha_receita.delete()
        messages.success(self.request, 'Receita excluída com sucesso!!!!')

        return redirect(reverse('autores:dashboard'))

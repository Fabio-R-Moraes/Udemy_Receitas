from django.urls import reverse, resolve
from receitasApp import views
from .test_receitas_base import ReceitasTestBase

class ReceitasReceitaViewsTest(ReceitasTestBase):
    def test_receitas_receita_view_esta_correta(self):
        view = resolve(
            reverse('receitas:receita', kwargs={'pk': 1})
        )
        self.assertIs(view.func.view_class, views.ReceitaDetail)

    def test_receitas_receita_view_retorna_404_se_nao_encontrar_receita(self):
        response = self.client.get(
            reverse('receitas:receita', kwargs={'pk': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_receitas_receita_template_carrega_a_receita_correta(self):
        titulo_necessario = 'Esta é uma página sobre modo de preparo - Carrega uma única receita'  # noqa: E501
        # Precisa de uma receita para fazer o teste
        self.faca_receita(titulo=titulo_necessario)
        response = self.client.get(
            reverse(
                'receitas:receita',
                kwargs={
                    'pk': 1
                }
            ))

        # Verificação por conteúdo
        response_content = response.content.decode('utf-8')

        self.assertIn(titulo_necessario, response_content)

    def test_receitas_receita_nao_carrega_receita_nao_publicadas(self):
        # Precisa de uma receita para fazer o teste
        receita = self.faca_receita(esta_publicado=False)

        response = self.client.get(
            reverse(
                'receitas:receita',
                kwargs={
                    'pk': receita.id
                }
            ))

        self.assertEqual(response.status_code, 404)

    def test_receitas_pesquisa_usando_a_view_correta(self):
        resolved = resolve(reverse('receitas:pesquisa'))

        self.assertIs(resolved.func.view_class, views.ReceitaListViewPesquisa)

    def test_receitas_pesquisa_carregue_o_template_correto(self):
        response = self.client.get(reverse('receitas:pesquisa') + '?q=teste')
        self.assertTemplateUsed(response, 'receitas/pesquisa.html')

    def test_receitas_procura_sem_termo_levanta_um_404(self):
        url = reverse('receitas:pesquisa')
        print(f'Resposta: {url}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

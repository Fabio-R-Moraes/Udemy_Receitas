from django.urls import reverse, resolve
from receitasApp import views
from .test_receitas_base import ReceitasTestBase

class ReceitasCategoriaViewsTest(ReceitasTestBase):
    def test_receitas_categoria_view_esta_correta(self):
        view = resolve(
            reverse('receitas:categoria', kwargs={'categoria_id': 1000})
        )
        self.assertIs(view.func, views.categoria)

    def test_receitas_categoria_view_retorna_404_se_nao_encontrar_receita(self):  # noqa: E501
        response = self.client.get(
            reverse('receitas:categoria', kwargs={'categoria_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_receitas_categoria_template_carrega_receitas(self):
        titulo_necessario = 'Este é um teste de categoria'
        # Precisa de uma receita para fazer o teste
        self.faca_receita(titulo=titulo_necessario)
        response = self.client.get(reverse('receitas:categoria', args=(1,)))

        # Verificação por conteúdo
        response_content = response.content.decode('utf-8')

        self.assertIn(titulo_necessario, response_content)

    def test_receitas_categoria_nao_carrega_receitas_nao_publicadas(self):
        # Precisa de uma receita para fazer o teste
        receita = self.faca_receita(esta_publicado=False)
        response = self.client.get(
            reverse('receitas:receita', kwargs={'id': receita.categoria.id})
        )

        self.assertEqual(response.status_code, 404)
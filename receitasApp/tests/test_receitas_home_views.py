from django.urls import reverse, resolve
from receitasApp import views
from .test_receitas_base import ReceitasTestBase
from unittest.mock import patch

class ReceitasHomeViewsTest(ReceitasTestBase):
    # Testes para a página HOME
    def test_receitas_home_view_esta_correta(self):
        view = resolve(reverse('receitas:home'))
        self.assertIs(view.func, views.home)

    def test_receitas_home_view_retorna_status_codigo_200_ok(self):
        response = self.client.get(reverse('receitas:home'))
        self.assertEqual(response.status_code, 200)

    def test_receitas_home_view_carrega_template_correto(self):
        response = self.client.get(reverse('receitas:home'))
        self.assertTemplateUsed(response, 'receitas/home.html')

    def test_receitas_home_mostrar_receitas_nao_encontradas(self):
        # Receitas.objects.get(pk=1).delete()
        response = self.client.get(reverse('receitas:home'))
        self.assertIn(
            '<h1>Não há receitas para mostrar...</h1>',
            response.content.decode('utf-8')
        )

        # Aplicar para causar uma falha de propósito
        # self.fail('Para que eu possa terminar de digitá-lo!!!')

    def test_receitas_home_template_carrega_receitas(self):
        # Precisa de uma receita para fazer o teste
        self.faca_receita(autor_data={
            'first_name': 'Fábio'
        })
        response = self.client.get(reverse('receitas:home'))

        # Verificação por contexto
        # response_receitas = response.context['receitas']
        # self.assertEqual(response_receitas.first().titulo, 'Repolho Cremoso')

        # Verificação por conteúdo
        response_content = response.content.decode('utf-8')
        response_context_receitas = response.context['receitas']

        self.assertIn('Repolho Cremoso', response_content)
        self.assertIn('Fábio', response_content)
        self.assertIn('2 porções', response_content)
        self.assertEqual(len(response_context_receitas), 1)

    def test_receitas_home_nao_carrega_receitas_nao_publicadas(self):
        # Precisa de uma receita para fazer o teste
        self.faca_receita(esta_publicado=False)
        response = self.client.get(reverse('receitas:home'))

        self.assertIn(
            '<h1>Não há receitas para mostrar...</h1>',
            response.content.decode('utf-8')
        )

    @patch('receitasApp.views.POR_PAGINA', new=4)
    def test_receitas_home_esta_paginado(self):
        # Precisa de varias receita para fazer o teste
        for i in range(12):
            kwargs = {'autor_data': {
                'username': f'Fabio_{i}'}, 'slug': f'bundinha_{i}'}
            self.faca_receita(**kwargs)

        response = self.client.get(reverse('receitas:home'))
        receitas = response.context['receitas']
        paginacao = receitas.paginator

        self.assertEqual(paginacao.num_pages, 3)
        self.assertEqual(len(paginacao.get_page(1)), 4)
        self.assertEqual(len(paginacao.get_page(2)), 4)

    def test_invalid_page_query_uses_page_one(self):
        # Precisa de varias receita para fazer o teste
        for i in range(12):
            kwargs = {'autor_data': {
                'username': f'Fabio_{i}'}, 'slug': f'bundinha_{i}'}
            self.faca_receita(**kwargs)

        with patch('receitasApp.views.POR_PAGINA', new=4):
            response = self.client.get(reverse('receitas:home') + '?page=1A')
            self.assertEqual(
                response.context['receitas'].number,
                1
            )

            response = self.client.get(reverse('receitas:home') + '?page=2')
            self.assertEqual(
                response.context['receitas'].number,
                2
            )


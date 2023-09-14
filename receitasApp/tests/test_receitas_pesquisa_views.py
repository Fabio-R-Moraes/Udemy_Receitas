from django.urls import reverse, resolve
from receitasApp import views
from .test_receitas_base import ReceitasTestBase

class ReceitasPesquisaViewsTest(ReceitasTestBase):
    def test_receitas_pesquisa_usando_a_view_correta(self):
        resolved = resolve(reverse('receitas:pesquisa'))
        self.assertIs(resolved.func.view_class, views.ReceitaListViewPesquisa)

    def test_receitas_pesquisa_carregue_o_template_correto(self):
        response = self.client.get(reverse('receitas:pesquisa') + '?q=teste')
        self.assertTemplateUsed(response, 'receitas/pesquisa.html')

    def test_receitas_procura_sem_termo_levanta_um_404(self):
        url = reverse('receitas:pesquisa')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_receitas_termo_procurado_esta_no_titulo_da_pagina_e_com_escape(self):  # noqa: E501
        url = reverse('receitas:pesquisa') + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            'Pesquisando por &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8')
        )

    def test_receitas_pesquisa_encontrar_receitas_pelo_titulo(self):
        titulo1 = 'Este é o primeiro título'
        titulo2 = 'Este é o segundo título'

        receita1 = self.faca_receita(
            slug='um',
            titulo=titulo1,
            autor_data={'username': 'Viviane Tetuda'}
        )
        receita2 = self.faca_receita(
            slug='dois',
            titulo=titulo2,
            autor_data={'username': 'Denise Cuzona'}
        )

        url_procurada = reverse('receitas:pesquisa')
        response1 = self.client.get(f'{url_procurada}?q={titulo1}')
        response2 = self.client.get(f'{url_procurada}?q={titulo2}')
        response_both = self.client.get(f'{url_procurada}?q=Este')

        self.assertIn(receita1, response1.context['receitas'])
        self.assertNotIn(receita2, response1.context['receitas'])

        self.assertIn(receita2, response2.context['receitas'])
        self.assertNotIn(receita1, response2.context['receitas'])

        self.assertIn(receita1, response_both.context['receitas'])
        self.assertIn(receita2, response_both.context['receitas'])
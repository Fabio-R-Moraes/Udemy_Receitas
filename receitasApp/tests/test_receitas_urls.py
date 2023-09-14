from django.test import TestCase
from django.urls import reverse

class ReceitaURLSTest(TestCase):
    def test_receitas_home_url_esta_correto(self):
        url = reverse('receitas:home')
        self.assertEqual(url, '/')

    def test_receitas_categoria_url_esta_correto(self):
        url = reverse('receitas:categoria', kwargs={'categoria_id': 1})
        self.assertEqual(url, '/receitas/categoria/1/')

    def test_receitas_receita_url_esta_correto(self):
        url = reverse('receitas:receita', kwargs={'pk': 1})
        self.assertEqual(url, '/receitas/1/')

    def test_receitas_pesquisa_url_esta_correta(self):
        url = reverse('receitas:pesquisa')
        self.assertEqual(url, '/receitas/pesquisa/')

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AutorLogoutTest(TestCase):
    def test_user_tries_logout_using_get_method(self):
        User.objects.create_user(username='meu_usuário', password='Flum1n3ns3#')
        self.client.login(username='meu_usuário', password='Flum1n3ns3#')

        response = self.client.get(reverse('autores:logout'), follow=True)

        self.assertIn(
            'Solicitação de logout inválida!',
            response.content.decode('utf-8')
        )

    def test_user_tries_logout_another_user(self):
        User.objects.create_user(username='meu_usuário', password='Flum1n3ns3#')
        self.client.login(username='meu_usuário', password='Flum1n3ns3#')

        response = self.client.post(
            reverse('autores:logout'),
            data={
                'username': 'outro_usuário'
            },
            follow=True
        )

        self.assertIn(
            'Você está tentando sair com OUTRO usuário!!!',
            response.content.decode('utf-8')
        )

    def test_user_can_logout_successfully(self):
        User.objects.create_user(username='meu_usuário', password='Flum1n3ns3#')
        self.client.login(username='meu_usuário', password='Flum1n3ns3#')

        response = self.client.post(
            reverse('autores:logout'),
            data={
                'username': 'meu_usuário'
            },
            follow=True
        )

        self.assertIn(
            'Usuário deslogado com sucesso!!!',
            response.content.decode('utf-8')
        )

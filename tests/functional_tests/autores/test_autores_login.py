import pytest
from .base import AutoresBaseTest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

@pytest.mark.functional_test
class AutoresLoginTest(AutoresBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_senha = 'MinhaSenh2'
        usuario = User.objects.create_user(username='meu_usuario', password=string_senha)

        #Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('autores:login'))
        formulario = self.browser.find_element(By.CLASS_NAME, 'main-form')
        usuario_field = self.get_by_placeholder(formulario, 'Digite o seu usuário')
        senha_field = self.get_by_placeholder(formulario, 'Informe a sua senha')

        #Usuário digita os dados pedidos
        usuario_field.send_keys(usuario.username)
        senha_field.send_keys(string_senha)
        formulario.submit()

        #Usuário vê a mensagem de login com suxcesso e seu nome
        self.assertIn(
            f'Você está logado com {usuario.username}',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
        #self.sleep()

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url +
            reverse('autores:login_create')
        )

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
        #self.sleep()

    def test_form_login_is_invalid(self):
        #Usuário abre a página de login
        self.browser.get(
            self.live_server_url +
            reverse('autores:login')
        )

        #Usuário vê o formulário de login
        formulario = self.browser.find_element(By.CLASS_NAME, 'main-form')

        #Tenta enviar valores vazios
        usuario = self.get_by_placeholder(formulario, 'Digite o seu usuário')
        senha = self.get_by_placeholder(formulario, 'Informe a sua senha')
        usuario.send_keys(' ')
        senha.send_keys(' ')

        #Envia o formulário
        formulario.submit()

        #Vê uma mensagem de erro na tela
        self.assertIn(
            'Usuário ou Senha inválidos!!!',
            self.browser.find_element(By.TAG_NAME, 'body').text
            )
        #self.sleep()

    def test_form_login_invalid_credentials(self):
        #Usuário abre a página de login
        self.browser.get(
            self.live_server_url +
            reverse('autores:login')
        )

        #Usuário vê o formulário de login
        formulario = self.browser.find_element(By.CLASS_NAME, 'main-form')

        #Tenta enviar valores que não existem
        usuario = self.get_by_placeholder(formulario, 'Digite o seu usuário')
        senha = self.get_by_placeholder(formulario, 'Informe a sua senha')
        usuario.send_keys('usuário_inválido')
        senha.send_keys('senha_inválida')

        #Envia o formulário
        formulario.submit()

        #Vê uma mensagem de erro na tela
        self.assertIn(
            'Credenciais inválidas...',
            self.browser.find_element(By.TAG_NAME, 'body').text
            )
        #self.sleep()

from .base import AutoresBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest

@pytest.mark.functional_test
class AutoresRegisterTest(AutoresBaseTest):
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/autores/register')
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('vivitetuda@email.com')

        callback(form)
        return form

    def test_empty_nome_error_message(self):
        def callback(form):
            nome_field = self.get_by_placeholder(form, 'Seu nome')
            nome_field.send_keys(' ')
            nome_field.send_keys(Keys.ENTER)

            #self.sleep(6)
            form = self.get_form()
            self.assertIn('Escreva o seu nome', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_sobrenome_error_message(self):
        def callback(form):
            sobrenome_field = self.get_by_placeholder(form, 'Seu sobrenome')
            sobrenome_field.send_keys(' ')
            sobrenome_field.send_keys(Keys.ENTER)

            #self.sleep(6)
            form = self.get_form()
            self.assertIn('Escreva seu sobrenome', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_usuario_error_message(self):
        def callback(form):
            usuario_field = self.get_by_placeholder(form, 'Seu nome de usuário')
            usuario_field.send_keys(' ')
            usuario_field.send_keys(Keys.ENTER)

            #self.sleep(6)
            form = self.get_form()
            self.assertIn('Este campo é obrigatório.', form.text)

        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, 'Digite seu e-mail')
            email_field.send_keys('email@invalid')
            email_field.send_keys(Keys.ENTER)

            #self.sleep(6)
            form = self.get_form()
            self.assertIn('Digite seu melhor e-mail', form.text)

        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match(self):
        def callback(form):
            senha_field = self.get_by_placeholder(form, 'Digite sua senha')
            senha1_field = self.get_by_placeholder(form, 'Confirme sua senha')
            senha_field.send_keys('P@ssw0rd')
            senha1_field.send_keys('P@ssw0rd_Diferente')
            senha1_field.send_keys(Keys.ENTER)

            #self.sleep(6)
            form = self.get_form()
            self.assertIn('Senha e Senha2 precisam ser iguais...', form.text)

        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_succesfully(self):
        self.browser.get(self.live_server_url + '/autores/register')
        form = self.get_form()
        self.get_by_placeholder(form, 'Seu nome de usuário').send_keys('Deninha')
        self.get_by_placeholder(form, 'Digite seu e-mail').send_keys('denni1@terra.com.br')
        self.get_by_placeholder(form, 'Seu nome').send_keys('Denise')
        self.get_by_placeholder(form, 'Seu sobrenome').send_keys('Freitas de Oliveira')
        self.get_by_placeholder(form, 'Digite sua senha').send_keys('T3tinhas')
        self.get_by_placeholder(form, 'Confirme sua senha').send_keys('T3tinhas')

        form.submit()
        self.sleep(10)
        self.assertIn(
            'Seu usuário foi criado, por favor, faça o login',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

from unittest import TestCase
from django.test import TestCase as djangoTestCase
from autoresApp.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse

class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username','Seu nome de usuário'),
        ('email', 'Digite seu e-mail'),
        ('first_name', 'Seu nome'),
        ('last_name', 'Seu sobrenome'),
        ('password', 'Digite sua senha'),
        ('password2', 'Confirme sua senha'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        placeholderCampo = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, placeholderCampo)

    @parameterized.expand([
        ('username', ('Obrigatório. 150 caracteres ou menos. '
                'Letras, números e @/./+/-/_ apenas.')),
        ('email', 'Digite seu melhor e-mail'),
        ('password', (
            'A senha precisa ter ao menos uma letra maiúscula,'
            'ao menos uma letra minúscula e um número. Também é necessário'
            'que tenha ao menos 8 caracteres...'
        )),
    ])
    def test_fields_help_text_is_correct(self, field, necessario):
        form = RegisterForm()
        atual = form[field].field.help_text
        self.assertEqual(atual, necessario)

    @parameterized.expand([
        ('username', 'Usuário'),
        ('email', 'E-mail'),
        ('first_name', 'Nome'),
        ('last_name', 'Sobrenome'),
        ('password', 'Senha'),
        ('password2', 'Senha2'),
    ])
    def test_fields_labels_is_correct(self, field, necessario):
        form = RegisterForm()
        atual = form[field].field.label
        self.assertEqual(atual, necessario)

class AuthorRegisterFormIntegrationTest(djangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@any.com',
            'password': 'Str0ngP2ssw0rd1',
            'password2': 'Str0ngP2ssw0rd1'
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'Este campo é obrigatório.'),
        ('first_name', 'Escreva o seu nome'),
        ('last_name', 'Escreva seu sobrenome'),
        ('email', 'Informe um e-mail válido...'),
        ('password', 'A senha não pode ser vazia...'),
        ('password2', 'A confirmação da senha não pode ser vazia...'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('autores:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        #self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_shoud_be_4(self):
        self.form_data['username'] = 'joa'
        url = reverse('autores:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Esse campo não pode ter menos de 4 caracteres!!!'

        # self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_shoud_be_150(self):
        self.form_data['username'] = 'F' * 151
        url = reverse('autores:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Certifique-se de que o valor tenha no máximo 150 caracteres'

        # self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('autores:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = (
            'ATENÇÃO: A senha precisa ter ao menos uma letra maiúscula,'
            'ao menos uma letra minúscula e um número. Também é necessário'
            'que tenha ao menos 8 caracteres...'
        )

        # self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

        self.form_data['password'] = '@A123abc123'
        url = reverse('autores:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc123t'
        url = reverse('autores:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Senha e Senha2 precisam ser iguais...'

        # self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

        self.form_data['password2'] = '@A123abc123'
        url = reverse('autores:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))
        #self.assertIn(msg, response.context['form'].errors.get('password'))

    def test_send_get_requests_to_registration_create_view_returns_404(self):
        url = reverse('autores:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse('autores:register_create')
        self.client.post(url, data=self.form_data, follow=True)

        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'O e-mail do usuário já está sendo usado!!!'

        self.assertIn(msg, response.context['form'].errors.get('email'))
        # self.assertIn(msg, response.content.decode('utf-8'))

    def test_author_created_can_login(self):
        url = reverse('autores:register_create')
        self.form_data.update({
            'username': 'testuser',
            'password': 'Abc12345678',
            'password2': 'Abc12345678',
        })
        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='testuser',
            password='Abc12345678'
        )

        self.assertTrue(is_authenticated)


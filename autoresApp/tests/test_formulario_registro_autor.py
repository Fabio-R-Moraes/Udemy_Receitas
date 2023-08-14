from django.test import TestCase
from autoresApp.forms import RegisterForm
from parameterized import parameterized

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
        ('username', 'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'),
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
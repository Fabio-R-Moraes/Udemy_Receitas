from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import novo_placeholder, senha_forte
class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        novo_placeholder(self.fields['username'], 'Seu nome de usuário')
        novo_placeholder(self.fields['email'], 'Digite seu e-mail')
        novo_placeholder(self.fields['first_name'], 'Seu nome')
        novo_placeholder(self.fields['last_name'], 'Seu sobrenome')
        novo_placeholder(self.fields['password'], 'Digite sua senha')
        novo_placeholder(self.fields['password2'], 'Confirme sua senha')

    username = forms.CharField(
        label = 'Usuário',
        help_text=('Obrigatório. 150 caracteres ou menos. '
                   'Letras, números e @/./+/-/_ apenas.'),
        error_messages={
            'required': 'Este campo é obrigatório.',
            'min_length': 'Esse campo não pode ter menos de 4 caracteres!!!',
            'max_length': 'Certifique-se de que o valor tenha no máximo 150 caracteres',
        },
        min_length=4, max_length=150
    )

    first_name = forms.CharField(
        required=True,
        label='Nome',
        error_messages={'required':'Escreva o seu nome'}
    )

    last_name = forms.CharField(
        required=True,
        label='Sobrenome',
        error_messages={'required': 'Escreva seu sobrenome'}
    )

    email = forms.EmailField(
        required=True,
        label='E-mail',
        error_messages={'required': 'Deixe seu melhor e-mail...'},
        help_text='Digite seu melhor e-mail'
    )

    password = forms.CharField(
        required=True,
        label= 'Senha',
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'A senha não pode ser vazia...'
        },
        help_text=(
            'A senha precisa ter ao menos uma letra maiúscula,'
            'ao menos uma letra minúscula e um número. Também é necessário'
            'que tenha ao menos 8 caracteres...'
        ),
        validators=[senha_forte],
    )

    password2 = forms.CharField(
        required=True,
        label='Senha2',
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'A confirmação da senha não pode ser vazia...'
        },
    )
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            ]
        #exclude = ['first_name']
        #labels = {
        #    'username': 'Usuário',
        #}

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'O e-mail do usuário já está sendo usado!!!', code='invalid',
            )

        return email

    def clean(self):
        dados = super().clean()
        password = dados.get('password')
        password2 = dados.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'Senha e Senha2 precisam ser iguais...',
                'password2': 'Senha e Senha2 precisam ser iguais...'
            })

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def novos_atributos(campo, nome_atributo, novo_valor):
    atributo_existente = campo.widget.attrs.get(nome_atributo, '')
    campo.widget.attrs[nome_atributo] = f'{atributo_existente} {novo_valor}'.strip()

def novo_placeholder(campo, valor):
    #campo.widget.attrs['placeholder'] = valor
    novos_atributos(campo, 'placeholder', valor)

def senha_forte(password):
    expressao = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not expressao.match(password):
        raise ValidationError((
            'A senha precisa ter ao menos uma letra maiúscula,'
            'ao menos uma letra minúscula e um número. Também é necessário'
            'que tenha ao menos 8 caracteres...'
        ),
            code='Invalid'
        )

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        novo_placeholder(self.fields['username'], 'Seu nome de usuário')
        novo_placeholder(self.fields['email'], 'Digite seu e-amil')
        novo_placeholder(self.fields['first_name'], 'Seu nome')
        novo_placeholder(self.fields['last_name'], 'Seu sobrenome')

    password2 = forms.CharField(
        required=True,
        label='Senha2',
        error_messages={
            'required': 'A senha não pode ser vazia...'
        },
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua senha'
        }),
        validators=[senha_forte],
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
        labels = {
            'username': 'Usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'password': 'Senha',
        }

        help_texts = {
            'email': 'Digite seu melhor e-mail',
        }

        error_messages = {
            'username': {
                'required': 'Esse campo não pode ser vazio!!!',
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Aqui fica seu primeiro nome...',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Invente sua senha...'
            }),
        }


    def clean(self):
        dados = super().clean()
        password = dados.get('password')
        password2 = dados.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'Senha e Senha2 precisam ser iguais...',
                'password2': 'Senha e Senha2 precisam ser iguais...'
            })

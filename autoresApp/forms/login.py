from django import forms
from utils.django_forms import novo_placeholder
class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        novo_placeholder(self.fields['username'], 'Digite o seu usuário')
        novo_placeholder(self.fields['password'], 'Informe a sua senha')

    username = forms.CharField(
        label='Usuário'
    )

    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput()
    )

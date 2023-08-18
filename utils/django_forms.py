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
            'ATENÇÃO: A senha precisa ter ao menos uma letra maiúscula,'
            'ao menos uma letra minúscula e um número. Também é necessário'
            'que tenha ao menos 8 caracteres...'
        ),
            code='Invalid'
        )
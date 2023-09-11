from django import forms
from receitasApp.models import Receitas
from utils.django_forms import novos_atributos
from utils.strings import e_um_numero_positivo
from collections import defaultdict
from django.core.exceptions import ValidationError

class AutoresReceitaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.meus_erros = defaultdict(list)

        novos_atributos(self.fields.get('modo_preparo'), 'class', 'span-2')
        #novos_atributos(self.fields.get('receita_imagem'), 'class', 'span-2')
    class Meta:
        model=Receitas
        fields= 'titulo', 'descricao', 'tempo_preparo', 'unidade_tempo_preparo', \
        'porcoes', 'unidade_porcoes', 'modo_preparo', 'receita_imagem'

        widgets= {
            'receita_imagem': forms.FileInput(
                attrs= {
                    'class': 'span-2'
                }
            ),
            'unidade_tempo_preparo': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            ),
            'unidade_porcoes': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            )
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        cleaned_data = self.cleaned_data
        titulo = cleaned_data.get('titulo')
        descricao = cleaned_data.get('descricao')

        if titulo == descricao:
            self.meus_erros['titulo'].append('Título e Descrição não podem ser iguais!!!')
            self.meus_erros['descricao'].append('Descrição e Título não podem ser iguais!!!')


        if self.meus_erros:
            raise ValidationError(self.meus_erros)

        return super_clean

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')

        if len(titulo) < 5:
            self.meus_erros['titulo'].append('O título deve ter mais de 5 caracteres...')

        return titulo

    def clean_tempo_preparo(self):
        nome_campo = 'tempo_preparo'
        valor_campo = self.cleaned_data.get(nome_campo)

        if not e_um_numero_positivo(valor_campo):
            self.meus_erros[nome_campo].append('O valor precisa ser positivo!!!')

        return valor_campo

    def clean_porcoes(self):
        nome_campo = 'porcoes'
        valor_campo = self.cleaned_data.get(nome_campo)

        if not e_um_numero_positivo(valor_campo):
            self.meus_erros[nome_campo].append('O valor precisa ser positivo!!!')

        return valor_campo
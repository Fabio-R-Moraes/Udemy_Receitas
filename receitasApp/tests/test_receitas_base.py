from django.test import TestCase
from receitasApp.models import Categoria, Receitas, User

class ReceitaMixing:
    def faca_categoria(self, nome='Jantar'):
        return Categoria.objects.create(nome=nome)

    def faca_autor(
        self,
        first_name='Wania',
        last_name='Puta',
        username='puta_gorda',
        password='fbrql823',
        email='chuparola@gmail.com',
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def faca_receita(
        self,
        categoria_data=None,
        autor_data=None,
        titulo='Repolho Cremoso',
        descricao='Um delicioso repolho cremoso',
        slug='repolho-cremoso',
        tempo_preparo=15,
        unidade_tempo_preparo='Minutos',
        porcoes=2,
        unidade_porcoes='porções',
        modo_preparo='Modo de preparo do repolho cremoso',
        modo_preparo_html=False,
        esta_publicado=True,
    ):

        if categoria_data is None:
            categoria_data = {}

        if autor_data is None:
            autor_data = {}

        return Receitas.objects.create(
            categoria=self.faca_categoria(**categoria_data),
            autor=self.faca_autor(**autor_data),
            titulo=titulo,
            descricao=descricao,
            slug=slug,
            tempo_preparo=tempo_preparo,
            unidade_tempo_preparo=unidade_tempo_preparo,
            porcoes=porcoes,
            unidade_porcoes=unidade_porcoes,
            modo_preparo=modo_preparo,
            modo_preparo_html=modo_preparo_html,
            esta_publicado=esta_publicado,
        )

    def faca_receita_em_lote(self, qtde=10):
        receitas = []
        for i in range(qtde):
            kwargs = {
                'titulo': f'Alargando o anel {i}',
                'slug': f'bundinha_{i}',
                'autor_data': {'username': f'Fabio_{i}'}
            }
            receita = self.faca_receita(**kwargs)
            receitas.append(receita)

        return receitas

class ReceitasTestBase(TestCase, ReceitaMixing):
    def setUp(self) -> None:
        return super().setUp()


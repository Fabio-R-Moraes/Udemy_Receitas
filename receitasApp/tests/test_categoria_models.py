from .test_receitas_base import ReceitasTestBase
from django.core.exceptions import ValidationError

class ReceitaCategoriaModelTest(ReceitasTestBase):
    def setUp(self) -> None:
        self.categoria = self.faca_categoria(
            nome='Almoço de Domingo'
        )
        return super().setUp()

    def test_categoria_representacao_da_string(self):
        self.assertEqual(
            str(self.categoria), self.categoria.nome,
        )

    def test_max_length_do_campo_nome_categoria_com_65_caracteres(self):
        self.categoria.nome = 'B' * 66
        with self.assertRaises(ValidationError):
            self.categoria.full_clean()
from unittest import TestCase
from paginacao import make_pagination_range

class PaginacaoTest(TestCase):
    def test_fazer_um_range_de_paginacao_retornar_um_range_de_paginacao(self):
        paginacao = make_pagination_range(
            range_pagina=list(range(1, 21)),
            qtd_paginas=4,
            pagina_atual=1
        )['paginacao']

        self.assertEqual([1, 2, 3, 4], paginacao)

    def test_faca_o_range_do_meio_ficar_correto(self):
        # Página Atual=10, Quantidade de Página= 2, Página do Meio = 2
        # Aqui o range DEVE mudar
        paginacao = make_pagination_range(
            range_pagina=list(range(1, 21)),
            qtd_paginas=4,
            pagina_atual=10,
        )['paginacao']

        self.assertEqual([9, 10, 11, 12], paginacao)

        # Página Atual=12, Quantidade de Página= 2, Página do Meio = 2
        # Aqui o range DEVE mudar
        paginacao = make_pagination_range(
            range_pagina=list(range(1, 21)),
            qtd_paginas=4,
            pagina_atual=12,
        )['paginacao']

        self.assertEqual([11, 12, 13, 14], paginacao)

    def test_faca_o_range_de_paginacao_estatico_se_a_ultima_pagina_estiver_no_range(self): # noqa E501
        # Página Atual=18, Quantidade de Página= 2, Página do Meio = 2
        # Aqui o range DEVE mudar
        paginacao = make_pagination_range(
            range_pagina=list(range(1, 21)),
            qtd_paginas=4,
            pagina_atual=14,
        )['paginacao']

        self.assertEqual([13, 14, 15, 16], paginacao)

        # Página Atual=19, Quantidade de Página= 2, Página do Meio = 2
        # Aqui o range DEVE mudar
        paginacao = make_pagination_range(
            range_pagina=list(range(1, 21)),
            qtd_paginas=4,
            pagina_atual=15,
        )['paginacao']

        self.assertEqual([14, 15, 16, 17], paginacao)

        # Página Atual=20, Quantidade de Página= 2, Página do Meio = 2
        # Aqui o range DEVE mudar
        paginacao = make_pagination_range(
            range_pagina=list(range(1, 21)),
            qtd_paginas=4,
            pagina_atual=16,
        )['paginacao']

        self.assertEqual([15, 16, 17, 18], paginacao)

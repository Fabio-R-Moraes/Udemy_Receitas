from selenium.webdriver.common.by import By
from .base import ReceitaBaseFunctionalTest
import pytest
from unittest.mock import patch
from selenium.webdriver.common.keys import Keys

@pytest.mark.functional_test
class ReceitaHomePageFunctionalTest(ReceitaBaseFunctionalTest):
    def test_receita_home_page_without_receitas_not_found_message(self):
        self.browser.get(self.live_server_url)
        temp = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Não há receitas para mostrar...', temp.text)

    @patch('receitasApp.views.POR_PAGINA', new=3)
    def test_receita_procura_input_encontrando_receitas(self):
        #Fabricando receitas
        receitas = self.faca_receita_em_lote()
        tituloNecessario = 'Viviane chupa rola e dá o cú... Tetuda!!'
        receitas[0].titulo = tituloNecessario
        receitas[0].save()
        #Usuario abre a pagina
        self.browser.get(self.live_server_url)
        #Encontra um campo de busca com o texto <Pesquise por uma receita...>
        procuraInput = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Pesquise por uma receita..."]'
        )
        #Clica nesse input e digita um termo de busca
        #para encontrar a receita com esse título
        #procuraInput.click()
        procuraInput.send_keys(tituloNecessario)
        procuraInput.send_keys(Keys.ENTER)

        #Usuário vê a receita que estava procurando
        self.assertIn(
            tituloNecessario,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text,
        )

        self.sleep(6)

    @patch('receitasApp.views.POR_PAGINA', new=3)
    def test_receita_home_page_pagination(self):
        # Fabricando receitas
        self.faca_receita_em_lote()
        # Usuario abre a pagina
        self.browser.get(self.live_server_url)
        #Vê que tem uma paginação e clica na página 2
        pagina2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Vá para a página 2"]',
        )
        pagina2.click()
        #Vê que tem 3 novas receitas na página 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            3
        )

        self.sleep(6)

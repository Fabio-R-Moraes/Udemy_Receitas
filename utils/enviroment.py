import os
#from dotenv import load_dotenv
#load_dotenv()

def get_env_variaveis(nome_variavel, variavel_padrao=''):
    return os.environ.get(nome_variavel, variavel_padrao)

def parse_separar_virgula_str_to_list(virgula_str):
    if not virgula_str or not isinstance(virgula_str, str):
        return []

    return  [string.strip() for string in virgula_str.split(',') if string]

if __name__ == '__main__':
    print(parse_separar_virgula_str_to_list(get_env_variaveis('ALLOWED_HOSTS')))
    print(parse_separar_virgula_str_to_list(''))
    print(parse_separar_virgula_str_to_list(12344))
    print(parse_separar_virgula_str_to_list('a, b, c'))

import io
import json
import re

import pandas as pd

def cleaner(text):
    text = text.lower()

    # substituir caracteres acentuados por não acentuados
    text = re.sub(r'[áàâãä]', 'a', text)
    text = re.sub(r'[éèêë]', 'e', text)
    text = re.sub(r'[íìîï]', 'i', text)
    text = re.sub(r'[óòôõö]', 'o', text)
    text = re.sub(r'[úùûü]', 'u', text)
    text = re.sub('ç', 'c', text)

    # remover todos os caracteres que não são números e não são letras (caracter de linha, de parágrafo etc)
    text = re.sub(r'[^a-z0-9]', '', text)

    return text


def read_csv(data):
    file = io.BufferedReader(data.get("planilha"))
    df = pd.read_table(file, sep=';', encoding='utf-8', engine='python')
    # colunas_a_procurar= ['TIPO', 'PRODUTO', 'LOJA', 'DEPARTAMENTO', 'AREA', 'UNIDADE CONTAGEM',
    #                    'UNIDADE COMPRA', 'MÉDIA DE REQUISIÇÃO']
    # colunas_a_procurar = [item.upper() for item in colunas_a_procurar]
    # df_novo = df[colunas_a_procurar]
    # del df

    # cria json somente string
    js = df.to_json(orient='records', force_ascii=False)

    # transforma json string em dict
    produtos_a_cadastrar = json.loads(js)

    return produtos_a_cadastrar


def get_unidade_por_nome(unidades, nome):
    for unidade in unidades:
        if cleaner(unidade.nome) == nome:
            return unidade
            
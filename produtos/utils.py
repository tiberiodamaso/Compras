import io
import json

import pandas as pd


def read_csv(data):
    file = io.BufferedReader(data.get("planilha"))
    df = pd.read_table(file, sep=';', encoding='utf-8', engine='python')

    # cria json somente string
    js = df.to_json(orient='records', force_ascii=False)

    # transforma json string em dict
    produtos_a_cadastrar = json.loads(js)

    return produtos_a_cadastrar

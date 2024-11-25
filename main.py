import functions_framework
import requests
from google.cloud import bigquery
from datetime import datetime

@functions_framework.http
def bitcoin(request):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,usd",
        "vs_currencies": "usd,brl"
    }

    response = requests.get(url, params=params)
    data = response.json()

    btc_usd = data["bitcoin"]["usd"]
    btc_brl = data["bitcoin"]["brl"]
    usd_brl = data["usd"]["brl"]

    save_to_bigquery(btc_usd, btc_brl, usd_brl)

    return {"status": "Data saved successfully", "data": data}

def save_to_bigquery(btc_usd, btc_brl, usd_brl):
    client = bigquery.Client()
    project_id = "projeto-etl-442220"
    dataset_id = "bitcoin"
    table_id = "raw_bitcoin"
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    timestamp = datetime.utcnow().isoformat()
    row_to_insert = {
        "btc_usd": btc_usd,
        "btc_brl": btc_brl,
        "usd_brl": usd_brl,
        "timestamp": timestamp
    }

    try:
        errors = client.insert_rows_json(table_ref, [row_to_insert])
        if errors:
            print(f"Erros ao inserir dados no BigQuery: {errors}")
        else:
            print("Dados inseridos com sucesso no BigQuery.")
    except Exception as e:
        print(f"Erro ao conectar ao BigQuery: {e}")
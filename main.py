import functions_framework

import requests

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

  return data
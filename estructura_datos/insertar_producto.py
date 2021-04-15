import requests
import json
url = "https://contabilidad.coopbarcelona.com/api/resource/Item"
api_key = "9d26609d5e4422e"
api_secret = "6b45fe9a3b83872"
headers = {
    'Authorization': "token " + api_key + ":" + api_secret
}
item = {
    "item_code": "Nombre Producto para Venta",
    "item_group": "Todos los Grupos de Artículos",
    "is_purchase_item": 0,
    "is_sales_item": 1,
    "is_stock_item": 0,
    "include_item_in_manufacturing": 0,
    "is_fixed_asset": 0,
    "item_defaults": [
        {
            "income_account": "420100 - INGRESOS POR INVERSIONES - CB"
        }
    ]
}
x = requests.request("POST",url,data=json.dumps(item), headers=headers)
print(x.json())
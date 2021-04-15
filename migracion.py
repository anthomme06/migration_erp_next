import requests
import json
import pandas as pd
api_key = "9d26609d5e4422e"
api_secret = "6b45fe9a3b83872"
headers = {
    'Authorization': "token " + api_key + ":" + api_secret
}

url_post_productos = "https://contabilidad.coopbarcelona.com/api/resource/Item"
col_productos = [
    "item_group",
    "item_name",
    "is_stock_item",
    "is_fixed_asset",
    "is_purchase_item",
    "expense_account",
    "is_sales_item",
    "income_account"
]
productos = pd.read_excel('productos.xlsx', usecols=col_productos)
productos = productos.fillna("")

def insertar_productos(df,url):
    for row in df.iterrows():
        item = {
            "item_code": row[1]['item_name'],
            "item_group": row[1]['item_group'],
            "is_purchase_item": row[1]['is_purchase_item'],
            "is_sales_item": row[1]['is_sales_item'],
            "is_stock_item": row[1]['is_stock_item'],
            "include_item_in_manufacturing": 0,
            "is_fixed_asset": row[1]['is_fixed_asset'],
            "item_defaults": [
                {
                    "income_account": row[1]['income_account'],
                    "expense_account": row[1]['expense_account']
                }
            ]
        }
        print(item)
        if requests.request("POST", url, data=json.dumps(item), headers=headers):
            print("Producto " + row[1]['item_name'] + " creado")
        else:
            print("Producto: " + row[1]['item_name'] + " no pudo ser creado")

insertar_productos(productos,url_post_productos)
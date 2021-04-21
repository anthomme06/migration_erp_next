import requests
import json
import pandas as pd
api_key = "9d26609d5e4422e"
api_secret = "6b45fe9a3b83872"
headers = {
    'Authorization': "token " + api_key + ":" + api_secret
}

url_base = "https://contabilidad.coopbarcelona.com/api/resource/"
url_productos = url_base + "Item"
url_proveedor = url_base + "Supplier"
url_pi = url_base + "Purchase Invoice"

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
col_proveedores = [
    "tax_id",
    "supplier_name",
    "id_type",
    "supplier_type",
    "supplier_group",
    "country"
]
col_pi = [
    "docstatus",
    "naming_series",
    "supplier",
    "tax_id",
    "posting_date",
    "due_date",
    "credit_to",
    "bill_no",
    "item_code",
    "qty",
    "rate",
    "expense_account"
]

productos = pd.read_excel('productos.xlsx', usecols=col_productos).fillna("")
proveedor = pd.read_excel(
    'proveedores.xlsx', usecols=col_proveedores).fillna("")
pi = pd.read_excel('facturas_de_compra_test2.xlsx', usecols=col_pi).fillna("")

# [print(proveedor[columna][fila]) for fila in proveedor.index for columna in proveedor.columns]


def create_item(df, url):
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
        if requests.request("POST", url, data=json.dumps(item), headers=headers):
            print("Producto " + row[1]['item_name'] + " creado")
        else:
            print("Producto: " + row[1]['item_name'] + " no pudo ser creado")


def create_supplier(df, url):
    for row in df.iterrows():
        row[1]['tax_id'] = row[1]['tax_id'].replace("-", "")
        item = {
            "tax_id": row[1]['tax_id'],
            "id_type": row[1]['id_type'],
            "supplier_name": row[1]['supplier_name'],
            "supplier_type": row[1]['supplier_type'],
            "supplier_group": row[1]['supplier_group'],
            "country": row[1]['country']
        }
        if requests.request("POST", url, data=json.dumps(item), headers=headers):
            print("Proveedor " + row[1]['supplier_name'] + " creado")
        else:
            print("Proveedor: " + row[1]
                  ['supplier_name'] + " no pudo ser creado")


def delete_records(df, url, column_name):
    '''
    Elimina los registros que se encuentren en el dataframe pasado,
    column_name = nombre del documento a eliminar
    '''
    url_delete = url
    for row in df.iterrows():
        url = url_delete + "/" + row[1][column_name]
        if requests.request("DELETE", url, headers=headers):
            print(row[1][column_name] + " ELIMINADO")
        else:
            print(row[1][column_name] + " no pudo ser ELIMINADO")


def find_supplier(url, rnc):
    rnc = rnc.replace('-', '')
    url = url + "?filters=[[\"Supplier\",\"tax_id\",\"=\",\"" + rnc + "\"]]"
    respuesta = requests.request("GET", url, headers=headers)
    try:
        respuesta.json()['data'][0]['name']
        return True
    except:
        return False


# def create_purchase_invoices(df, url):
#     for row in df.iterrows():
#         items = [{
#             "item_code": row[1]['item_code'],
#             "qty": row[1]['qty'],
#             "rate": row[1]['rate'],
#             "expense_account": row[1]['expense_account']
#         }]
#         while not row[1]['item_code']:

#             items = items.append
#             items = {
#                 "item_code": row[1]['item_code'],
#                 "qty": row[1]['qty'],
#                 "rate": row[1]['rate'],
#                 "expense_account": row[1]['expense_account']
#             }
#         if requests.request("POST", url, data=json.dumps(item), headers=headers):
#             print("Factura de Compra: " + str(row[1]['tax_id']) + " creado")
#         else:
#             print("Factura de Compra: " +
#                   str(row[1]['tax_id']) + " no pudo ser creado*******")

def find_supplier_by_name(url, name):
    url = url + "?filters=[[\"Supplier\",\"name\",\"=\",\"" + name + "\"]]&fields=[\"name\",\"tax_id\"]"
    respuesta = requests.request("GET", url, headers=headers)
    try:
        return respuesta.json()['data'][0]['tax_id']
        # respuesta.json()['data'][0]['name']
        return True
    except:
        return False

# create_item(productos, url_productos)
# create_supplier(proveedor, url_proveedor)
# delete_records(proveedor,url_proveedor,"supplier_name")
# print(find_supplier(url_proveedor,"130563748"))
# create_purchase_invoices(pi, url_pi)
print(find_supplier_by_name(url_proveedor,"SEGUROS UNIVERSAL"))
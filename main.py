#Librerias Requeridas:
#request
#Flask
#requests-toolbelt
#pip install request, Flask, requests-toolbelt

import requests
import json
from flask import Flask, request
from requests_toolbelt import MultipartEncoder

app = Flask(__name__)

"""
Método llamado get_shop que implementa una API de tipo GET
ruta: http://127.0.0.1:5000/api/v1/get_shop
Parametros:
----------
comuna_nombre : String, formato Json
    Parámetro filtro que indica la comuna de la farmacia 
local_nombre : String, formato Json
    Parámetro filtro que indica el nombre de la farmacia 
Retorna:
-------
Response http status code
    Retorna el status code que corresponde y en caso de 200 retorna el valor de las farmacias filtradas
"""
@app.route('/api/v1/get_shop', methods=['GET'])
def get_shop():
    try:
        #Variable de respuesta al cliente de tipo http status
        response_data = None

        # EL consumo a la API obtener comunas no se utiliza más adelante, ya que se filtra por comuna directamente en la API de Locales
        encoder = MultipartEncoder({'reg_id': '7'})
        response_comunas = requests.post(
            'https://midastest.minsal.cl/farmacias/maps/index.php/utilidades/maps_obtener_comunas_por_regiones',
            data=encoder, headers={'Content-Type': encoder.content_type})
        comunas = (response_comunas.content).decode("utf8")

        #Obtener filtros al consumir API del Body formato JSON
        parameters_input = request.get_json()

        #Validamos si viene el parametro 'comuna_nombre' dentro del Body en Formato JSON
        if 'comuna_nombre' in parameters_input:
            comuna = parameters_input['comuna_nombre']
        else:
            response_data = ('No existe parámetro de entrada comuna_nombre', 400)

        # Validamos si viene el parametro 'local_nombre' dentro del Body en Formato JSON
        if 'local_nombre' in parameters_input:
            name_shop = parameters_input['local_nombre']
        else:
            response_data = ('No existe parámetro de entrada local_nombre', 400)

        if response_data is None:
            response = requests.get('https://farmanet.minsal.cl/maps/index.php/ws/getLocalesRegion?id_region=7')
            if (response.status_code == 200):
                #Se obtiene las farmacias
                data_shops = json.loads((response.content).decode("utf8"))
                data_shops = [[x['local_nombre'],x['local_direccion'],x['local_telefono'],x['local_lat'],x['local_lng']] for x in data_shops if x['comuna_nombre'] == comuna.upper().strip() and x['local_nombre'] == name_shop.upper().strip()]

                #Si se obtiene Data según los filtros entonces se retorna información en formato Json.
                if len(data_shops) > 0:
                    response_data = json.dumps(data_shops)
                else:
                    response_data = ('', 204)
            else:
                response_data = ('', response.status_code)
    except Exception as e:
        response_data = (str(e), 500)
    return response_data

if __name__ == '__main__':
    app.run(debug=True)

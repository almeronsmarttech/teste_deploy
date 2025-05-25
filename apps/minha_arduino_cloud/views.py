from django.shortcuts import render
from django.conf import settings
from arduino_iot_cloud import ArduinoCloudClient
#from arduino_iot_cloud.configuration import Configuration
#from arduino_iot_cloud.apis.properties_v2_api import PropertiesV2Api

"""
def get_client():
    config = Configuration(
        client_id=settings.ARDUINO_CLIENT_ID,
        client_secret=settings.ARDUINO_CLIENT_SECRET
    )
    return ArduinoCloudClient(config)

def sensores_view(request):
    return render(request, "minha_arduino_cloud/sensores.html")

def sensores_partial_view(request):
    client = get_client()
    properties_api = PropertiesV2Api(client)
    properties = properties_api.things_properties_list(settings.THING_ID)

    dados = []
    for prop in properties:
        dados.append({
            "nome": prop.name,
            "valor": prop.last_value,
            "atualizado": prop.last_value_updated_at[:19].replace("T", " ") if prop.last_value_updated_at else "",
        })

    return render(request, "minha_arduino_cloud/_painel_sensores.html", {"dados": dados})
"""
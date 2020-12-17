from flask import jsonify, json
from app.models.turno import Turno
from app.models.centro import Centro
from app.models.tipocentro import TipoCentro
import requests

def tipos_mas_utilizados():
    """
    Cantidad de turnos de cada hora
    """
    centros = Centro.tipos_mas_utilizados()

    array = []
    for item in centros:
        tipo = TipoCentro.buscar_id(item[0])
        diccionario = {
            "tipo": tipo.nombre,
            "cantidad": item[1],
        }
        array.append(diccionario)

    return jsonify({"tiposmasutilizados": array})

def municipios_mas_concurridos():
    """
    Los municipios con más turnos
    """
    centros = Centro.municipios_mas_concurridos()

    array = []
    for item in centros:
        req = requests.get(
            "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios/"+item[0]
        )
        Jresponse = req.text
        data = json.loads(Jresponse)
        cant = Turno.cantidad(item[1])
        diccionario = {
            "municipio": data["data"]["Town"][item[0]]["name"],
            "cantidad": cant,
        }
        array.append(diccionario)

    return jsonify({"municipiosmasconcurridos": array})
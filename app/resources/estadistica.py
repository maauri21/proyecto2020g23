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
            "cant": item[1],
        }
        array.append(diccionario)

    return {
          "columns": ['tipo', 'cant'],
          "rows": 
              array
        }

def municipios_mas_concurridos():
    """
    Los municipios con más turnos
    """
    centros = Centro.municipios_mas_concurridos()

    array = []
    for item in centros:
        req = requests.get(
            "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios/"+(item[0])
        )
        Jresponse = req.text
        data = json.loads(Jresponse)
        cant = Turno.cantidad(item[1])
        diccionario = {
            "municipio": data["data"]["Town"][item[0]]["name"],
            "cantidad": cant,
        }
        if (cant != 0):
            array.append(diccionario)

    return {
          "columns": ['municipio', 'cantidad'],
          "rows": 
                array
        }

def fases_de_municipios():
    """
    La cantidad de municipios de cada fase
    """
    tot = str(json.loads(requests.get(
        "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios"
    ).text)['total'])

    req = requests.get(
        "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?page=1&per_page="+tot
    )
    Jresponse = req.text
    data = json.loads(Jresponse)

    array = []
    fases = {


    }
      
    for fase,contenido in data["data"]["Town"].items():
           
        if (contenido["phase"])in fases.keys():
            fases[contenido["phase"]]+=1
        else:
            fases[contenido["phase"]]=1      
 
    
    for fase,cantidad in fases.items():
        array.append({"fase": 'Fase '+str(fase),
        "cantidad": cantidad})
    
    return {
          "columns": ['fase', 'cantidad'],
          "rows": 
                array
        }
    
        
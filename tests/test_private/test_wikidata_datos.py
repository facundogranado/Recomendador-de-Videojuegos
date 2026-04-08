import pytest
import requests_mock
from src.store import CATALOGO_JUEGOS

def test_obtener_juego_id_existe_pero_no_es_videojuego(client):
    """GET /juegos/{id} con un QID que existe pero no es P31=Q7889 devuelve 404."""
    with requests_mock.Mocker() as m:
        m.get(
            "https://www.wikidata.org/w/api.php",
            json={
                "entities": {
                    "Q42": {
                        "id": "Q42",
                        "claims": {
                            "P31": [{"mainsnak": {"datavalue": {"value": {"id": "Q5"}}}}]
                        },
                        "labels": {"es": {"value": "Douglas Adams"}}
                    }
                }
            },
        )
        resp = client.get("/juegos/Q42")
        assert resp.status_code == 404


def test_juegos_fuente_wikidata_datos_incompletos(client):
    """GET /juegos?q=X&fuente=wikidata con datos faltantes en claims no debe crashear (200)."""
    with requests_mock.Mocker() as m:
        # 1. Mock de búsqueda
        m.get("https://www.wikidata.org/w/api.php?action=wbsearchentities", 
              json={"search": [{"id": "Q_INCOMPLETO"}]})
        
        # 2. Mock de entidad sin fecha ni género
        m.get("https://www.wikidata.org/w/api.php?action=wbgetentities", 
              json={
                  "entities": {
                      "Q_INCOMPLETO": {
                          "id": "Q_INCOMPLETO",
                          "labels": {"es": {"value": "Juego Incompleto"}},
                          "claims": {
                              "P31": [{"mainsnak": {"datavalue": {"value": {"id": "Q7889"}}}}]
                          }
                      }
                  }
              })
        
        resp = client.get("/juegos?q=incompleto&fuente=wikidata")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data[0]["nombre"] == "Juego Incompleto"
        assert data[0]["lanzamiento"] == ""
        assert data[0]["genero"] == ""

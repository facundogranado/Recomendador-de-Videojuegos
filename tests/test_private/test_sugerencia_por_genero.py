"""
Tests que debés implementar: sugerencia con filtro por género.
Completar los tests según el contrato de la API.
"""

import pytest
from conftest import JUEGO_TEST_ID

def test_sugerencia_con_genero_solo_devuelve_ese_genero(client):
    r = client.post("/usuarios", json={"nombre": "Sug"})
    assert r.status_code == 201
    uid = r.get_json()["id"]

    r_juegos = client.get("/juegos?q=zelda&fuente=wikidata")
    assert r_juegos.status_code == 200
    juegos = r_juegos.get_json()
    genero = juegos[0]["genero"]

    r_add = client.post(
        f"/usuarios/{uid}/juegos",
        json={
            "juego_id": JUEGO_TEST_ID,
            "tengo": True,
            "quiero": False,
            "jugado": False,
            "me_gusta": False,
        },
    )
    assert r_add.status_code == 201

    resp = client.get(f"/usuarios/{uid}/sugerencia?genero={genero}")

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["genero"] == genero


def test_sugerencia_genero_sin_coincidencias_404(client):
    r = client.post("/usuarios", json={"nombre": "Sug"})
    uid = r.get_json()["id"]

    client.get("/juegos?q=zelda&fuente=wikidata")

    client.post(
        f"/usuarios/{uid}/juegos",
        json={
            "juego_id": JUEGO_TEST_ID,
            "tengo": True,
            "quiero": False,
            "jugado": False,
            "me_gusta": False,
        },
    )

    r = client.get(f"/usuarios/{uid}/sugerencia?genero=NoExiste")
    assert r.status_code == 404
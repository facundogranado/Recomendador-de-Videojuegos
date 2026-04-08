# Recomendador de Videojuegos

Proyecto base para implementar la API según el contrato en `openapi.yaml`. El archivo **openapi.yaml** define los endpoints; las rutas están registradas en **app.py** y la lógica de cada una se implementa en los módulos de **src/** (usuarios, juegos, sugerencias, wikidata, filtros).

## Requisitos

- **Docker (recomendado)** para ejecutar la API y el grading sin instalar Python localmente.
- Alternativa: Python 3.10 o superior, venv y `pip install -r requirements.txt`.


## Configuración y uso

### Con Docker (recomendado)

```bash
make docker-build
make docker-run
```

Con la API corriendo, abrí **http://localhost:5000/docs**. Para verificar tests, cobertura, lint y complejidad sin tener Python local:

```bash
make docker-grade
```

Necesitás un archivo `.env` en la raíz (copiá desde `.env.example`). Los datos se persisten en SQLite (por defecto `instance/datos.db`). Para volver a empezar con datos vacíos: `make clean-db`.

### Alternativa con venv

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # Opcional: WIKIDATA_USER_AGENT para llamadas a Wikidata
make run
```
Si no usás make: `PYTHONPATH=. python3 -m src.app`.

- `make test` — Ejecuta los tests
- `make grade` — Ejecuta el script de grading (tests + cobertura + lint + complejidad)
- `make lint` — Ruff y radon
- `make clean-db` — Borra la base SQLite para empezar de cero con datos vacíos

Los tests en **test_metrics.py** comprueban estilo (ruff) y complejidad ciclomática.
- app.py: punto de entrada de la aplicación Flask.
- usuarios.py: manejo de usuarios.
- juegos.py: lógica de juegos.
- wikidata.py: integración con API externa.
- store.py: persistencia en SQLite.
- auth.py: autenticación.
- /test: tests privados y publicos.


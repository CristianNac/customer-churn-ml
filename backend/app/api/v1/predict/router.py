import io
from pathlib import Path

import pandas as pd

from fastapi import APIRouter, HTTPException, Request, Response, UploadFile



router = APIRouter(prefix='/predict', tags=['predict'])

TIPO_ARCHIVO = {'.csv'}
MAX_BYTES = 5 * 1024 * 1024
UMBRAL = 0.5


@router.post('/batch')
async def subir_archivo(archivo:UploadFile, request:Request):
    # Validar extensión
    ext = Path(archivo.filename or '').suffix.lower()
    if ext not in TIPO_ARCHIVO:
        raise HTTPException(415, f"Extensión no permitida {ext}")
    # Validar tamaño
    contenido = await archivo.read()
    if len(contenido) > MAX_BYTES:
        raise HTTPException(413, "Archivo demasiado grande (Max 5 mb)")
#     #Leer el CSV
    try:
        df = pd.read_csv(io.BytesIO(contenido))
    except (pd.errors.ParserError, UnicodeDecodeError):
        df = pd.read_csv(io.BytesIO(contenido), sep=';', encoding='latin-1')

    if df.empty:
        raise HTTPException(422, "El CSV está vacío")
    
    #Validación de columnas
    requeridas = set(request.app.state.columnas_modelo)
    faltantes = requeridas - set(df.columns)
    if faltantes:
        raise HTTPException(422, f"Faltan columnas {sorted(faltantes)}")
    
    #Predecir
    model = request.app.state.model
    proba = model.predict_proba(df)[:,1]

    resultado = df.copy()
    resultado['probabilidad_churn'] = proba.round(3)
    resultado['prediccion'] = (proba >= UMBRAL).astype(int)

    #Devolver como CSV descargable
    csv_texto = resultado.to_csv(index=False)

    return Response(
        content=csv_texto,
        media_type='text/csv',
        headers={"Content-Disposition": "attachment; filename=predicciones.csv"}
    )
    



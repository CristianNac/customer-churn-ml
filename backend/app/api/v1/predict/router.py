from pathlib import Path

from fastapi import APIRouter, HTTPException, Request, Response, UploadFile

from services.prediction_service import (
    ColumnasFaltantesError,
    CSVEmptyError,
    leer_csv,
    predecir,
    validar_columnas,
)

router = APIRouter(prefix='/predict', tags=['predict'])

TIPO_ARCHIVO = {'.csv'}
MAX_BYTES = 5 * 1024 * 1024

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
    requeridas = request.app.state.columnas_modelo
    try:
        df = leer_csv(contenido=contenido)
        validar_columnas(df, requeridas)
    except CSVEmptyError as e:
        raise HTTPException(422, e.message) from e
    except ColumnasFaltantesError as e:
        raise HTTPException(422, f"Faltan columnas {e.faltantes}") from e
     
    #Predecir
    model = request.app.state.model
    resultado = predecir(df=df, model=model)
    
    #Devolver como CSV descargable
    csv_texto = resultado.to_csv(index=False)

    return Response(
        content=csv_texto,
        media_type='text/csv',
        headers={"Content-Disposition": "attachment; filename=predicciones.csv"}
    )
    



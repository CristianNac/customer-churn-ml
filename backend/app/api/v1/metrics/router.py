import json

from services.metrics_service import read_metrics
from fastapi import APIRouter, HTTPException

from core.paths import METRIC_PATH

router = APIRouter(prefix='/metrics', tags=['metrics'])

@router.get('/')
def get_metrics():
    try:
        return read_metrics()

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404, detail='No se encontraron las métricas del modelo'
        ) from error
    
    except Exception as error:
        raise HTTPException(
            status_code=500, detail='Error al leer las métricas del modelo'
        ) from error
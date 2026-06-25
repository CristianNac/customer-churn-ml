import json

from fastapi import APIRouter

router = APIRouter(prefix='/metrics', tags=['metrics'])

@router.get('/')
def get_metrics():
    try:
        with open('../../../../metric_results/metrics_best_model.json') as file:
            return json.load(file) 
        
    except Exception as error:
        print(error)

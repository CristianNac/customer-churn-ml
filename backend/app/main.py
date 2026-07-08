from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1.metrics.router import router as metric_router
from api.v1.predict.router import router as predict_router
from core.ml import load_model  # noqa: F401



@asynccontextmanager
async def lifespan(app: FastAPI):
    model = load_model()
    app.state.model = model  
    app.state.columnas_modelo = model.named_steps['Selector'].columns_to_select
    print('Modelo cargado Exitosamente')

    yield

    app.state.model = None
    app.state.columnas_modelo = None
    print('Modelo removido de memoria. Servidor apagado')


def create_app() -> FastAPI:
    app = FastAPI(title='ML-Churn', lifespan = lifespan)
    app.include_router(metric_router)
    app.include_router(predict_router)
    return app

app = create_app()

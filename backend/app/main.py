from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1.metrics.router import router as metric_router
from core.ml import load_model  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_model()  
    print('Modelo cargado Exitosamente')

    yield

    app.state.model = None
    print('Modelo removido de memoria. Servidor apagado')


def create_app() -> FastAPI:
    app = FastAPI(title='ML-Churn', lifespan = lifespan)
    app.include_router(metric_router)
    return app

app = create_app()



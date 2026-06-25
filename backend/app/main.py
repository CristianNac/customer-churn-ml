from fastapi import FastAPI

from api.v1.metrics.router import router as metric_router


def create_app() -> FastAPI:
    app = FastAPI(title='ML-Churn')
    app.include_router(metric_router)
    return app

app = create_app()



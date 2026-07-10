# Predicción de Fuga de Clientes (Customer Churn)

> Proyecto de Machine Learning end-to-end que identifica qué clientes están por abandonar un servicio de telecomunicaciones y **explica por qué**, para que un equipo de retención pueda actuar a tiempo. Incluye desde el análisis exploratorio hasta una **API de predicción con FastAPI**, contenerizada con Docker y desplegada en la nube.

**🔗 Demo en vivo:** [ml-churn-model.onrender.com/docs](https://ml-churn-model.onrender.com/docs) — documentación interactiva de la API (Swagger UI).

> ⏳ Alojada en el plan gratuito de Render: si estuvo inactiva un rato, el primer acceso puede tardar ~30-60 s en "despertar". Es el comportamiento normal del _cold start_, no un error.

## El problema de negocio

Retener a un cliente cuesta mucho menos que conseguir uno nuevo. Este proyecto predice la probabilidad de que un cliente se dé de baja (_churn_) y, más importante, identifica los factores que más influyen en esa decisión, convirtiendo un modelo predictivo en recomendaciones accionables para el negocio.

## Resultados principales

- **Mejor modelo:** Regresión Logística con balanceo _NearMiss_
- **Desempeño sobre la clase _churn_ (conjunto de prueba):**

  | Métrica   | Valor |
  | --------- | ----- |
  | Recall    | 0.72  |
  | Precisión | 0.59  |
  | F1-score  | 0.65  |
  | Accuracy  | 0.79  |

  El modelo prioriza el **recall**: detecta ~72 % de los clientes que efectivamente se fugan, que es la métrica clave para un caso de retención (es más costoso dejar escapar a un cliente que contactar a uno que no se iba a ir).

- **Factores que más predicen la fuga (vía SHAP):**
  - **Antigüedad del cliente (`tenure`)** — el predictor más fuerte por amplio margen: a menor antigüedad, mayor riesgo de fuga.
  - **Pago con cheque electrónico** — el método de pago asociado al mayor aumento de probabilidad de churn.
  - **Cargos mensuales altos (`MonthlyCharges`)** — a mayor cobro mensual, mayor propensión a irse.
  - _Refuerzan el patrón:_ el contrato mes a mes y el internet de fibra óptica aumentan el riesgo; tener soporte técnico y seguridad online lo reducen.

<!-- Exporta tu gráfico beeswarm de SHAP a una carpeta /images y descomenta la línea de abajo -->
<!-- ![Importancia de variables (SHAP)](images/shap_beeswarm.png) -->

## Estructura del proyecto

```
Proyecto-Churn/
├── Notebooks/
│   ├── Eda_Telco_Churn.ipynb    # Análisis exploratorio: calidad de datos,
│   │                              # nulos, duplicados, balance de la variable
│   │                              # objetivo, correlaciones y distribuciones
│   └── models_churn.ipynb        # Pipelines de procesamiento, modelos
│                                  # (Regresión Logística + XGBoost), técnicas
│                                  # de balanceo y explicabilidad con SHAP
├── model_results/
│   └── resultados_modelos.csv    # Métricas comparativas de cada modelo probado
├── backend/                       # API de predicción (FastAPI)
│   ├── app/
│   │   ├── main.py                # Punto de entrada; carga el modelo al arrancar
│   │   ├── api/v1/
│   │   │   ├── metrics/           # Endpoint que expone las métricas del modelo
│   │   │   └── predict/           # Endpoint de predicción por lote (CSV)
│   │   ├── core/
│   │   │   ├── ml.py              # Carga del modelo serializado
│   │   │   ├── paths.py           # Rutas centralizadas del proyecto
│   │   │   └── transformers.py    # Transformers custom (ColumnSelector)
│   │   ├── services/              # Lógica de negocio (métricas y predicción)
│   │   ├── models/                # Pipelines y modelos entrenados (.skops)
│   │   └── metric_results/        # Métricas del mejor modelo (JSON)
│   ├── Makefile                   # Atajos: install, lint, format, typecheck, run
│   ├── Dockerfile                 # Imagen multi-stage para producción
│   └── pyproject.toml             # Dependencias gestionadas con uv
└── README.md
```

## Metodología

1. **EDA:** revisión de calidad de datos (nulos, duplicados, tipos), balance de la variable objetivo, correlaciones y distribuciones.
2. **Preprocesamiento:** pipelines de `scikit-learn` / `feature-engine` para evitar fuga de datos entre entrenamiento y prueba.
3. **Modelado:** Regresión Logística y XGBoost, comparando técnicas de balanceo de clases (class weight, SMOTE, NearMiss).
4. **Optimización:** búsqueda de hiperparámetros con Optuna.
5. **Explicabilidad:** importancia de variables mediante coeficientes y SHAP.
6. **Puesta en producción:** serialización del pipeline con `skops`, exposición a través de una API REST con FastAPI y una capa de _services_ que separa la lógica de negocio de los endpoints, contenerizada con Docker y desplegada en Render.

## Tecnologías

- **Lenguaje:** Python 3.13
- **Datos:** Pandas, Feature-engine
- **Modelado:** scikit-learn, imbalanced-learn, XGBoost, Optuna
- **Explicabilidad:** SHAP
- **Visualización:** Matplotlib, Seaborn
- **Persistencia:** skops
- **API:** FastAPI
- **Contenerización y despliegue:** Docker (imagen multi-stage), Render
- **Tooling:** uv (gestión de entorno y dependencias), Ruff (lint/format), mypy (type checking)

## Cómo ejecutarlo

### 1. Notebooks (análisis y entrenamiento)

Abre los notebooks en la carpeta `Notebooks/` para reproducir el EDA y el entrenamiento de los modelos.

### 2. API de predicción (backend)

El backend usa [uv](https://docs.astral.sh/uv/) para gestionar el entorno. Desde la carpeta `backend/`:

```bash
cd backend
make install   # uv sync — instala dependencias
make run       # uv run fastapi dev — levanta el servidor de desarrollo
```

Una vez arriba, la documentación interactiva queda disponible en `http://127.0.0.1:8000/docs`.

El endpoint principal, `POST /api/v1/predict/batch`, recibe un CSV con los datos de los clientes y devuelve otro CSV con la predicción de fuga para cada uno.

Otros comandos útiles (definidos en el `Makefile`):

```bash
make lint        # revisa el código con Ruff
make format      # corrige y ordena el código con Ruff
make typecheck   # revisa el tipado con mypy
```

### 3. Con Docker

El backend incluye un `Dockerfile` multi-stage que produce una imagen mínima de producción. Desde la carpeta `backend/`:

```bash
cd backend
docker build -t ml-churn:v1 .
docker run --rm -p 8000:8000 ml-churn:v1
```

La API queda disponible en `http://localhost:8000/docs`. La imagen lee la variable de entorno `PORT` (con 8000 por defecto), lo que la hace compatible con plataformas como Render.

## Roadmap

- [x] Análisis exploratorio (EDA)
- [x] Modelado y comparación (Regresión Logística, XGBoost, balanceo)
- [x] Explicabilidad con SHAP
- [x] Serialización del modelo con skops
- [x] Endpoint de métricas (FastAPI)
- [x] Endpoint de predicción por lote desde CSV (FastAPI)
- [x] Refactor a capa de _services_ (lógica de negocio separada de los endpoints)
- [x] Contenerización con Docker (imagen multi-stage)
- [x] Despliegue en la nube — [demo en vivo en Render](https://ml-churn-model.onrender.com/docs)
- [ ] CI/CD con GitHub Actions (lint + typecheck en cada push/PR)

## Autor

Cristian Orellana — [LinkedIn](https://www.linkedin.com/in/cristian-o7)

#**Proyecto para predecir fuga de clientes**

La idea de este proyecto es construir un modelo de Machine Learning que permita tomar decisiones de acuerdo a las características o variables que más influyen en la fuga de clientes.

#**Estructura del proyecto**

* Notebook/ Eda_Telco_Churn.ipynb: Este archivo contiene el análisis exploratorio, donde se revisa la calidad de los datos (Existencia de valores nulos, valores duplicados), también se analiza el balance de los datos para la variable predictora y también vemos correlaciones y distribución de variables.

* Notebook/ models_churn.ipynb: En este archivo se construyen Pipelines para procesar datos, además se prueban modelos de regresión logística con distintas técnicas de balanceo de datos y modelos XGBoost, también se revisa la influencia de las característias en la construcción de modelos usando los coeficientes de la regresión logística o la técnica de SHAP basada en la teoría de juegos.

* models/: Aquí se guardan los pipelines y modelos entrenados.

* metric_results/: Archivo csv donde se guardan las métricas para los distintos modelos.

#**Tecnologías**

- Python 3.13 
##**Librerías de visualización**
- Matplotlib
- Seaborn 
##**Librerías para entrenar modelos**
- sklearn
- imblearn
- xgboost
- Optuna 
##**Librerías para procesamiento de datos**
- Pandas
- Sklearn
- Feature Engine 
##**Librerías para explicabilidad de modelos**
- Shap

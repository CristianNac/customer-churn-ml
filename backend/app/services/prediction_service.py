import io

import pandas as pd

UMBRAL = 0.5

class CSVEmptyError(Exception):
    def __init__(self, message="El Csv está vacío"):
        self.message = message
        super().__init__(self.message)

class ColumnasFaltantesError(Exception):
    def __init__(self, faltantes, message="Faltan columnas"):
        self.faltantes = faltantes
        self.message = message
        super().__init__(self.message)

def leer_csv(contenido:bytes)->pd.DataFrame:
    try:
        df = pd.read_csv(io.BytesIO(contenido))

    except pd.errors.EmptyDataError:
        raise CSVEmptyError() from None

    except (pd.errors.ParserError, UnicodeDecodeError):
        df = pd.read_csv(io.BytesIO(contenido), sep=';', encoding='latin-1')
    
    if df.empty:
        raise CSVEmptyError()    
    return df

def validar_columnas(df:pd.DataFrame, requeridas)->None:
    faltantes = set(requeridas) - set(df.columns)
    if faltantes:
        raise ColumnasFaltantesError(faltantes=sorted(faltantes))
    
def predecir(df:pd.DataFrame, model)->pd.DataFrame:
    proba = model.predict_proba(df)[:,1]

    resultado = df.copy()
    resultado['probabilidad_churn'] = proba.round(3)
    resultado['prediccion'] = (proba >= UMBRAL).astype(int)
    return resultado



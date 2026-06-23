from fastapi import FastAPI

app = FastAPI(title='ML-Churn-Project')

@app.get('/')
def home():
    return 'Hola mundo'
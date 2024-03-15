from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def Aware():
    return 'Goodbye World TrollDespair'

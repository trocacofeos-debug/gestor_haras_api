from fastapi import FastAPI
from api.gerar_contrato import handler

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/gerar_contrato")
async def gerar():
    return {"sucesso": True}
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem
import os

app = FastAPI()

# Configuração para carregar o HTML da pasta 'templates'
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analise")
async def analise(request: Request, smiles: str = Form(...)):
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        # Criamos o dicionário de dados de forma limpa
        dados_moleculares = {
            "smiles": smiles,
            "mw": f"{Descriptors.MolWt(mol):.2f}",
            "logp": f"{Descriptors.MolLogP(mol):.2f}",
            "lipinski": "✅ Aprovada" if Descriptors.MolWt(mol) <= 500 else "⚠️ Alerta"
        }
        # O segredo está aqui: passamos um único dicionário final
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "res": dados_moleculares
        })
    else:
        # Caso o SMILES seja inválido
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "res": {"erro": "SMILES Inválido!"}
        })
    
    return templates.TemplateResponse("index.html", {"request": request, "result": results})

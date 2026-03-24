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

@app.post("/analyze")
async def analyze_molecule(request: Request, smiles: str = Form(...)):
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        results = {
            "smiles": smiles,
            "mw": f"{Descriptors.MolWt(mol):.2f}",
            "logp": f"{Descriptors.MolLogP(mol):.2f}",
            "donors": Descriptors.NumHDonors(mol),
            "acceptors": Descriptors.NumHAcceptors(mol),
            "lipinski": "✅ Aprovada" if Descriptors.MolWt(mol) <= 500 and Descriptors.MolLogP(mol) <= 5 else "⚠️ Alerta"
        }
    else:
        results = {"error": "SMILES Inválido. Verifique a estrutura."}
    
    return templates.TemplateResponse("index.html", {"request": request, "result": results})

import string
import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from models import SessionLocal, UrlShorting
from fastapi.responses import RedirectResponse

router = APIRouter()

def gerar_codigo(tamanho=6):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

def get_db():
     db = SessionLocal()
     try:
          yield db 
     finally:
          db.close()

@router.post("/shorten", response_model=schemas.UrlResponse)
async def criar_url(requisicao: schemas.UrlCreate, db: Session = Depends(get_db)):
   
    codigo = gerar_codigo()
   
    nova_url = models.UrlShorting(
        url_original=str(requisicao.url_original),
        url_encurtada=codigo,
        cliques=0
    )
     
    db.add(nova_url)
    db.commit()
    db.refresh(nova_url)
    
    return nova_url

@router.get("/stats/{code}")
async def mostrar_status(code: str, db: Session = Depends(get_db)):
     url_objeto = db.query(models.UrlShorting).filter(models.UrlShorting.url_encurtada==code).first()
     
     if not url_objeto:
          raise HTTPException(status_code=404, detail="Código não encontrado")
                 
     return {
          "status": "sucesso",
          "dados": {
              "url_original": url_objeto.url_original,
              "cliques": url_objeto.cliques
          }
     }

@router.get("/{code}")
async def redic_original(code: str, db: Session = Depends(get_db)):
    
     url_objeto = db.query(models.UrlShorting).filter(models.UrlShorting.url_encurtada==code).first()

     if not url_objeto:
          raise HTTPException(status_code=404, detail="Código não encontrado")
     
     url_objeto.cliques += 1
     db.commit()
     
     return RedirectResponse(url=url_objeto.url_original)
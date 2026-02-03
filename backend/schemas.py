from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

class UrlCreate(BaseModel):
    url_original: HttpUrl
    slug_personalizado: Optional[str] = Field(None, min_length=3, max_length=15)

class UrlResponse(BaseModel):
    url_original: str
    url_encurtada: str 
    cliques: int 
    
    class Config:
        from_attributes=True
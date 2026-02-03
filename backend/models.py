from  sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

db = create_engine("sqlite:///./banco.db")

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)

class UrlShorting(Base):
    __tablename__ = "urlshorting"
    
    id = Column(Integer, primary_key=True, index=True)
    url_original = Column(String, nullable=False)
    url_encurtada = Column(String, unique=True, index=True, nullable=False)
    cliques = Column(Integer, default=0)


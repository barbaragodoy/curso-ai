from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import upload, url_import, analytics, bd_pipeline
from app.database.mongo import ping_db
from app.database.postgres import ping_postgres

app = FastAPI(
    title="ETL Pipeline",
    description=(
        "Pipeline ETL para ingestão, tratamento e armazenamento de dados no MongoDB. "
        "Suporta CSV, JSONL e URL pública. "
        "Inclui pipeline para 3 arquivos JSONL com enriquecimento de documentos e comparação PostgreSQL."
    ),
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bd_pipeline.router)
app.include_router(upload.router)
app.include_router(url_import.router)
app.include_router(analytics.router)


@app.get("/health", tags=["Health"])
def health():
    mongo_ok    = ping_db()
    postgres_ok = ping_postgres()
    return {
        "status": "ok" if (mongo_ok and postgres_ok) else "degraded",
        "api": "online",
        "mongodb":    "connected" if mongo_ok    else "unreachable",
        "postgresql": "connected" if postgres_ok else "unreachable",
    }

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.pipeline.extractor import extract_from_url
from app.pipeline.quality import generate_quality_report
from app.pipeline.transformer import transform
from app.pipeline.loader import load, save_quality_report

router = APIRouter(prefix="/pipeline", tags=["Pipeline"])


class UrlImportRequest(BaseModel):
    url: str

    model_config = {
        "json_schema_extra": {
            "example": {"url": "https://raw.githubusercontent.com/user/repo/main/data.csv"}
        }
    }


@router.post("/url")
async def import_from_url(body: UrlImportRequest):
    """
    Importa dados de uma URL pública (CSV ou JSON), executa a pipeline ETL
    e armazena no MongoDB em uma collection derivada da URL.
    """
    url = str(body.url).strip()
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="A URL deve começar com http:// ou https://")

    try:
        df_raw = extract_from_url(url)

        if df_raw.empty:
            raise HTTPException(status_code=422, detail="Nenhum dado encontrado na URL informada.")

        quality_report = generate_quality_report(df_raw, source=f"url:{url}")
        df_clean = transform(df_raw, source="url", source_name=url)
        load_result = load(df_clean, source_name=url)
        report_id = save_quality_report(quality_report)

        return {
            "status": "success",
            "source": "url",
            "url": url,
            "collection_name": load_result["collection_name"],
            "quality_report": quality_report,
            "load_result": load_result,
            "quality_report_id": report_id,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

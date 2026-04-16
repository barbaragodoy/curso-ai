from fastapi import APIRouter, UploadFile, File, HTTPException
from app.pipeline.extractor import extract_from_csv
from app.pipeline.quality import generate_quality_report
from app.pipeline.transformer import transform
from app.pipeline.loader import load, save_quality_report

router = APIRouter(prefix="/pipeline", tags=["Pipeline"])


@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    """
    Recebe um arquivo CSV, executa a pipeline ETL e armazena no MongoDB.
    Cada arquivo é salvo em uma collection com o nome derivado do arquivo.
    """
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Apenas arquivos .csv são aceitos.")

    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Arquivo vazio.")

    try:
        df_raw = extract_from_csv(content, filename=file.filename)
        quality_report = generate_quality_report(df_raw, source=f"csv:{file.filename}")
        df_clean = transform(df_raw, source="csv", source_name=file.filename)
        load_result = load(df_clean, source_name=file.filename)
        report_id = save_quality_report(quality_report)

        return {
            "status": "success",
            "source": "csv",
            "filename": file.filename,
            "collection_name": load_result["collection_name"],
            "quality_report": quality_report,
            "load_result": load_result,
            "quality_report_id": report_id,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

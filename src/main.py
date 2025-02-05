from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Any
import logging
from datetime import datetime
from enum import Enum

from src.db.chroma import db_manager
from src.ingestion.document_processor import document_processor
from src.llm.manager import llm_manager

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG Document Management API",
    description="API de gestion documentaire avec RAG",
    version="2.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèles Pydantic simplifiés
class DocumentRequest(BaseModel):
    doc_id: str = Field(..., description="Identifiant unique du document")
    content: str = Field(..., description="Contenu du document")
    metadata: Dict[str, str] = Field(default_factory=dict, description="Métadonnées du document")

class SearchRequest(BaseModel):
    query: str
    n_results: int = Field(default=3, ge=1, le=10)

class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

# Cache pour le statut des traitements
processing_status = {}

@app.get("/")
async def read_root():
    return {
        "status": "online",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/add_document/", status_code=202)
async def api_add_document(request: DocumentRequest, background_tasks: BackgroundTasks):
    try:
        processing_status[request.doc_id] = ProcessingStatus.PENDING
        
        background_tasks.add_task(
            process_document_task,
            request.doc_id,
            request.content,
            request.metadata
        )

        return {
            "status": "accepted",
            "doc_id": request.doc_id,
            "message": "Document en cours de traitement",
            "status_endpoint": f"/status/{request.doc_id}"
        }

    except Exception as e:
        logger.error(f"Erreur lors de l'ajout du document: {str(e)}")
        processing_status[request.doc_id] = ProcessingStatus.FAILED
        raise HTTPException(status_code=500, detail=str(e))

async def process_document_task(doc_id: str, content: str, metadata: Dict):
    try:
        processing_status[doc_id] = ProcessingStatus.PROCESSING
        
        await document_processor.process_document(
            doc_id=doc_id,
            content=content,
            metadata=metadata
        )

        processing_status[doc_id] = ProcessingStatus.COMPLETED

    except Exception as e:
        logger.error(f"Erreur lors du traitement de {doc_id}: {str(e)}")
        processing_status[doc_id] = ProcessingStatus.FAILED
        raise

@app.get("/status/{doc_id}")
async def get_processing_status(doc_id: str):
    status = processing_status.get(doc_id, ProcessingStatus.PENDING)
    return {"doc_id": doc_id, "status": status}

@app.post("/search_documents/")
async def api_search_documents(request: SearchRequest):
    try:
        results = await db_manager.search_documents(
            query=request.query,
            n_results=request.n_results
        )
        return results
    except Exception as e:
        logger.error(f"Erreur lors de la recherche: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/document_versions/{doc_id}")
async def api_get_document_versions(doc_id: str):
    """Récupération de l'historique des versions"""
    try:
        result = await db_manager.get_document_versions(doc_id)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des versions: {str(e)}")
        # Retourner une réponse d'erreur plus détaillée
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des versions: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5010)
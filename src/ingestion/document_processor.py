from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List, Dict
import logging
from src.llm.manager import llm_manager
from src.db.chroma import db_manager

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.llm_manager = llm_manager
        self.db_manager = db_manager
        # Initialisation du text splitter avec des paramètres optimisés
        self.text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False
        )

    async def process_document(self, doc_id: str, content: str, metadata: Dict) -> Dict:
        """Traite un document avec analyse IA"""
        try:
            # Découper le document en chunks
            chunks = self.text_splitter.create_documents(
                texts=[content],
                metadatas=[{
                    "doc_id": doc_id,
                    "chunk_index": i,
                    **metadata
                } for i in range(len(content))]
            )
            
            logger.info(f"Document {doc_id} découpé en {len(chunks)} chunks")

            # Analyser le contenu avec le LLM
            analysis_result = await self.llm_manager.analyze_document(content)
            
            # Enrichir les métadonnées
            enriched_metadata = {
                **metadata,
                "ai_analysis": analysis_result["analysis"],
                "processed": True,
                "chunks_count": len(chunks)
            }

            # Stocker chaque chunk dans ChromaDB
            for i, chunk in enumerate(chunks):
                chunk_metadata = {
                    **enriched_metadata,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
                await self.db_manager.add_document(
                    doc_id=f"{doc_id}_chunk_{i}",
                    content=chunk.page_content,
                    metadata=chunk_metadata
                )

            return {
                "status": "success",
                "doc_id": doc_id,
                "analysis": analysis_result["analysis"],
                "metadata": enriched_metadata,
                "chunks_info": {
                    "total_chunks": len(chunks),
                    "avg_chunk_size": sum(len(c.page_content) for c in chunks) / len(chunks)
                }
            }
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement du document {doc_id}: {str(e)}")
            raise

    async def analyze_documents(self, doc_ids: List[str]) -> Dict:
        """Analyse comparative de plusieurs documents"""
        try:
            documents_content = []
            chunks_by_doc = {}

            # Récupérer tous les chunks pour chaque document
            for doc_id in doc_ids:
                chunks = await self.db_manager.get_document_chunks(doc_id)
                if chunks:
                    documents_content.append(" ".join(c["content"] for c in chunks))
                    chunks_by_doc[doc_id] = chunks

            if not documents_content:
                return {"error": "Aucun document trouvé"}

            prompt = """Analysez ces documents et fournissez :
            1. Points communs principaux
            2. Différences notables
            3. Recommandations globales
            4. Synthèse des points d'action

            Documents à analyser:"""

            for idx, doc in enumerate(documents_content, 1):
                prompt += f"\nDocument {idx}: {str(doc)}\n"

            analysis = await self.llm_manager.analyze_document(prompt)
            
            return {
                "status": "success",
                "comparative_analysis": analysis["analysis"],
                "documents_analyzed": len(documents_content),
                "chunks_info": {
                    doc_id: len(chunks) for doc_id, chunks in chunks_by_doc.items()
                }
            }

        except Exception as e:
            logger.error(f"Erreur lors de l'analyse comparative: {str(e)}")
            raise

document_processor = DocumentProcessor()
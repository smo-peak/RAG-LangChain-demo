import chromadb
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChromaDBManager:
    def __init__(self):
        """Initialisation de ChromaDB avec persistence"""
        try:
            self.client = chromadb.PersistentClient(path="/chroma/chroma")
            self.collection = self.client.get_or_create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("ChromaDB initialisé avec configurations optimisées")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de ChromaDB: {str(e)}")
            raise

    async def add_document(self, doc_id: str, content: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Ajoute un document dans ChromaDB avec métadonnées et versioning.
        """
        try:
            # Préparation des métadonnées
            if metadata is None:
                metadata = {}
            
            metadata.update({
                "date_added": datetime.utcnow().isoformat(),
                "version": 1
            })

            # Ajout du document
            self.collection.add(
                documents=[content],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            logger.info(f"Document {doc_id} ajouté avec succès")
            return {
                "message": f"Document {doc_id} ajouté avec succès",
                "metadata": metadata
            }

        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du document {doc_id}: {str(e)}")
            raise

    async def get_document_versions(self, doc_id: str) -> Dict:
        """Récupère l'historique des versions d'un document."""
        try:
            # Vérifier si le document existe
            try:
                results = self.collection.get(
                    ids=[doc_id],
                    include=["metadatas", "documents"]
                )
            except Exception as e:
                logger.error(f"Erreur lors de la récupération du document {doc_id}: {str(e)}")
                return {
                    "error": f"Document {doc_id} non trouvé ou erreur de récupération",
                    "versions": []
                }

            if not results['ids']:
                logger.info(f"Document {doc_id} non trouvé")
                return {
                    "error": f"Document {doc_id} non trouvé",
                    "versions": []
                }

            # Récupérer les informations du document
            versions = []
            try:
                current_metadata = results['metadatas'][0]
                current_content = results['documents'][0]

                versions.append({
                    "version": current_metadata.get('version', 1),
                    "metadata": {
                        "date_added": current_metadata.get('date_added', 'N/A'),
                        "author": current_metadata.get('author', 'N/A'),
                        "category": current_metadata.get('category', 'N/A'),
                        "source": current_metadata.get('source', 'N/A')
                    },
                    "content": current_content,
                    "is_current": True
                })

                return {
                    "status": "success",
                    "doc_id": doc_id,
                    "versions": versions
                }

            except Exception as e:
                logger.error(f"Erreur lors du traitement des métadonnées: {str(e)}")
                return {
                    "error": "Erreur lors du traitement des métadonnées",
                    "versions": []
                }

        except Exception as e:
            logger.error(f"Erreur inattendue lors de la récupération des versions de {doc_id}: {str(e)}")
            raise Exception(f"Erreur inattendue: {str(e)}")

    async def search_documents(
        self,
        query: str,
        n_results: int = 3,
        filters: Optional[Dict] = None,
        min_relevance_score: float = 0.7
    ) -> Dict:
        """Recherche sémantique avancée"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results * 2,  # Récupérer plus pour filtrer par score
                include=['documents', 'metadatas', 'distances']
            )

            if not results['documents'][0]:
                return {
                    "status": "success",
                    "results": [],
                    "total_candidates": 0,
                    "filtered_results": 0
                }

            # Traitement et filtrage des résultats
            processed_results = []
            for doc, meta, distance in zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            ):
                # Conversion de la distance en score de similarité
                similarity_score = 1 - (distance / 2)
                
                if similarity_score >= min_relevance_score:
                    processed_results.append({
                        "content": doc,
                        "metadata": meta,
                        "relevance_score": round(similarity_score, 3)
                    })

            # Trier par score et limiter aux n_results
            processed_results.sort(key=lambda x: x['relevance_score'], reverse=True)
            processed_results = processed_results[:n_results]

            return {
                "status": "success",
                "results": processed_results,
                "total_candidates": len(results['documents'][0]),
                "filtered_results": len(processed_results)
            }

        except Exception as e:
            logger.error(f"Erreur lors de la recherche: {str(e)}")
            raise

# Instance unique pour l'application
db_manager = ChromaDBManager()
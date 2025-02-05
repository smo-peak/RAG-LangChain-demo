from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import logging
from datetime import datetime
import time
import os

logger = logging.getLogger(__name__)

class LLMManager:
    def __init__(self):
        try:
            callback_manager = CallbackManager([
                StreamingStdOutCallbackHandler()
            ])
            
            # Récupération de l'URL d'Ollama depuis les variables d'environnement
            ollama_base_url = os.getenv('OLLAMA_HOST', 'http://ollama:11434')
            
            # Configuration de base de Mistral
            self.llm = Ollama(
                model="mistral",
                callback_manager=callback_manager,
                temperature=0.7,
                timeout=300,
                base_url=ollama_base_url
            )
            logger.info(f"LLM initialisé avec succès (URL: {ollama_base_url})")
            
        except Exception as e:
            logger.error(f"Erreur LLM init: {str(e)}")
            raise

    async def analyze_document(self, content: str, analysis_type: str = "default") -> dict:
        try:
            logger.info(f"Début analyse document type: {analysis_type}")
            start_time = time.time()
            
            # Sélection du prompt selon le type d'analyse
            if analysis_type == "detailed":
                prompt = self._get_detailed_prompt(content)
            else:
                prompt = self._get_standard_prompt(content)
            
            # Analyse avec le LLM
            response = self.llm.invoke(prompt)
            
            # Post-traitement de la réponse
            processed_response = self._process_llm_response(response)
            
            logger.info(f"Analyse terminée en {time.time() - start_time:.2f}s")
            return processed_response
            
        except Exception as e:
            logger.error(f"Erreur analyse: {str(e)}")
            raise

    def _get_detailed_prompt(self, content: str) -> str:
        return f"""Analysez ce document en détail et extrayez :
        1. Résumé exécutif
        2. Points principaux
        3. Objectifs identifiés
        4. Recommandations détaillées
        5. Points d'attention critiques
        6. Métriques clés
        7. Prochaines étapes suggérées

        Document: {content}
        """

    def _get_standard_prompt(self, content: str) -> str:
        return f"""Analysez ce document et extrayez :
        1. Points principaux
        2. Objectifs
        3. Recommandations
        4. Points d'attention

        Document: {content}
        """

    def _process_llm_response(self, response: str) -> dict:
        """Post-traitement de la réponse du LLM"""
        try:
            # Ajout de métadonnées et structuration
            return {
                "analysis": response,
                "timestamp": datetime.now().isoformat(),
                "model": "mistral",
                "version": "1.0"
            }
        except Exception as e:
            logger.error(f"Erreur processing: {str(e)}")
            return {"error": str(e)}

# Instance unique pour l'application
llm_manager = LLMManager()
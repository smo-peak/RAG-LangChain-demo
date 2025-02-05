import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

API_URL = "http://langchain-api:5010"
TIMEOUT = 240

def test_api_connection():
    try:
        response = requests.get(f"{API_URL}/", timeout=TIMEOUT)
        st.write("Status code:", response.status_code)
        st.write("Response:", response.json())
        return True
    except requests.exceptions.ConnectionError as e:
        st.error(f"Erreur de connexion : {str(e)}")
        return False
    except Exception as e:
        st.error(f"Erreur inattendue : {str(e)}")
        return False

def add_document(doc_id, content, auteur, categorie, source):
    try:
        data = {
            "doc_id": doc_id,
            "content": content,
            "metadata": {
                "author": auteur,
                "category": categorie,
                "source": source
            }
        }
        response = requests.post(
            f"{API_URL}/add_document/",
            json=data,
            timeout=TIMEOUT
        )
        if response.status_code == 202:
            return True, response.json()
        return False, response.text
    except requests.exceptions.Timeout:
        st.error("Timeout - Le serveur prend trop de temps à répondre")
        return False, "Timeout"
    except Exception as e:
        st.error(f"Erreur inattendue : {str(e)}")
        return False, str(e)

def get_document_versions(doc_id):
    try:
        response = requests.get(
            f"{API_URL}/document_versions/{doc_id}",
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            return True, response.json()
        elif response.status_code == 404:
            return False, "Document non trouvé"
        else:
            error_detail = response.json().get('detail', 'Erreur inconnue')
            return False, f"Erreur: {error_detail}"
    except requests.exceptions.RequestException as e:
        return False, f"Erreur de connexion : {str(e)}"
    except Exception as e:
        return False, f"Erreur inattendue : {str(e)}"

def search_documents(query, n_results=3):
    try:
        response = requests.post(
            f"{API_URL}/search_documents/",
            json={"query": query, "n_results": n_results},
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            return True, response.json()
        return False, response.text
    except Exception as e:
        st.error(f"Erreur lors de la recherche : {str(e)}")
        return False, str(e)

def format_metadata(metadata):
    formatted = {}
    for key, value in metadata.items():
        if isinstance(value, (dict, list)):
            formatted[key] = json.dumps(value, indent=2)
        else:
            formatted[key] = str(value)
    return formatted

def main():
    st.title("📂 Gestion des Documents avec LangChain & IA")
    
    tabs = st.tabs(["📝 Ajouter", "🔍 Rechercher", "📜 Versions"])
    
    with tabs[0]:
        with st.form(key="add_document_form"):
            doc_id = st.text_input("ID du document")
            content = st.text_area("Contenu du document")
            auteur = st.text_input("Auteur")
            categorie = st.text_input("Catégorie")
            source = st.text_input("Source")
            submit = st.form_submit_button("Ajouter et Analyser")
            
            if submit:
                if not doc_id or not content.strip():
                    st.error("⚠️ ID et Contenu sont requis!")
                else:
                    with st.spinner("🤖 Analyse en cours..."):
                        success, result = add_document(doc_id, content, auteur, categorie, source)
                        if success:
                            st.success("✅ Document ajouté!")
                            st.json(result)
    
    with tabs[1]:
        query = st.text_input("🔍 Rechercher", placeholder="Entrez votre recherche...")
        n_results = st.slider("Nombre de résultats", 1, 10, 3)
        
        if query:
            with st.spinner("Recherche en cours..."):
                success, results = search_documents(query, n_results)
                if success and results.get("results"):
                    for i, doc in enumerate(results["results"], 1):
                        with st.expander(f"Document {i} (Score: {doc['relevance_score']:.2f})"):
                            st.markdown("**Contenu:**")
                            st.write(doc["content"])
                            st.markdown("**Métadonnées:**")
                            formatted_metadata = format_metadata(doc["metadata"])
                            st.json(formatted_metadata)
                else:
                    st.info("Aucun résultat")
    
    with tabs[2]:
        doc_id_version = st.text_input("ID du document à vérifier")
        if doc_id_version:
            with st.spinner("Récupération des versions..."):
                success, versions_data = get_document_versions(doc_id_version)
                if success:
                    if isinstance(versions_data, dict) and "versions" in versions_data:
                        versions = versions_data["versions"]
                        if versions:
                            for version in versions:
                                with st.expander(f"Version {version.get('version', 'N/A')}"):
                                    st.markdown("**Contenu:**")
                                    st.write(version.get('content', 'N/A'))
                                    metadata = version.get('metadata', {})
                                    st.markdown("**Métadonnées:**")
                                    st.markdown(f"- Date: {metadata.get('date_added', 'N/A')}")
                                    st.markdown(f"- Auteur: {metadata.get('author', 'N/A')}")
                                    st.markdown(f"- Catégorie: {metadata.get('category', 'N/A')}")
                                    st.markdown(f"- Source: {metadata.get('source', 'N/A')}")
                                    if version.get('is_current'):
                                        st.info("Version actuelle")
                        else:
                            st.info("Aucune version trouvée pour ce document")
                    else:
                        st.error("Format de réponse inattendu")
                else:
                    st.error(versions_data)

if __name__ == "__main__":
    main()
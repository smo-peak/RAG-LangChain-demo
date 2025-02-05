#!/bin/bash

echo "🚀 Initialisation du projet LangChain Demo ESN..."

# Définition de la structure des dossiers
DIRECTORIES=(
    "src"
    "src/ingestion"
    "src/analysis"
    "src/comparison"
    "src/llm"
    "src/db"
    "src/reports"
    "src/ui"
    "scripts"
    "tests"
)

# Création des dossiers
for dir in "${DIRECTORIES[@]}"; do
    mkdir -p "$dir"
done

echo "📂 Dossiers créés."

# Création des fichiers essentiels avec du contenu de base

# Fichier .env
cat <<EOL > .env
# Variables d’environnement
# Configuration du stockage MinIO
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=password
MINIO_ENDPOINT=http://localhost:9000

# Configuration ChromaDB
CHROMA_DB_PATH=chroma_db

# Configuration Ollama pour LLM
OLLAMA_MODEL=mistral
OLLAMA_MEMORY_LIMIT=10GB
EOL
echo "⚙️ Fichier .env créé."

# Fichier .gitignore
cat <<EOL > .gitignore
# Ignore les fichiers sensibles et temporaires
.env
__pycache__/
chroma_db/
*.log
*.sqlite
EOL
echo "🚫 Fichier .gitignore créé."

# Fichier requirements.txt
cat <<EOL > requirements.txt
# Dépendances du projet
langchain
fastapi
streamlit
chromadb
sqlite
pandas
pytest
boto3  # Pour MinIO
ollama  # Pour Mistral 7B
EOL
echo "📦 Fichier requirements.txt créé."

# Fichier README.md
cat <<EOL > README.md
# LangChain Demo ESN 🚀

## 📌 Objectif du Projet
Ce projet est un démonstrateur utilisant **LangChain** et **Mistral 7B via Ollama** pour assister les consultants ESN dans l’analyse de documents et la modernisation des systèmes d’information.

## 📂 Architecture
- **Analyse de documents** : Extraction des insights et KPIs
- **Comparaison stratégique** : Alignement avec les objectifs business
- **Génération automatique de recommandations** : ROI, Impact CO₂, Roadmap

## 🛠️ Installation
1. **Clonez le repo :**
   \`\`\`bash
   git clone https://github.com/votre-repo/langchain-demo-esn.git
   cd langchain-demo-esn
   \`\`\`

2. **Installez les dépendances :**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Lancez le projet :**
   \`\`\`bash
   python main.py
   \`\`\`
EOL
echo "📖 Fichier README.md créé."

# Fichier docker-compose.yml
cat <<EOL > docker-compose.yml
version: '3.8'

services:
  minio:
    image: minio/minio
    container_name: minio
    ports:
      - "9000:9000"
    environment:
      MINIO_ACCESS_KEY: admin
      MINIO_SECRET_KEY: password
    command: server /data

  chromadb:
    image: chromadb/chromadb
    container_name: chromadb
    ports:
      - "8000:8000"
    volumes:
      - chromadb_data:/chroma_db

  langchain-api:
    build: .
    container_name: langchain-api
    ports:
      - "5000:5000"
    depends_on:
      - chromadb
      - minio
    env_file:
      - .env

volumes:
  chromadb_data:
EOL
echo "🐳 Fichier docker-compose.yml créé."

# Création d’un fichier main.py pour le point d’entrée du projet
cat <<EOL > main.py
import os

def main():
    print("🚀 Bienvenue dans le démonstrateur LangChain pour ESN")
    print("🌍 Chargement du modèle :", os.getenv("OLLAMA_MODEL", "mistral"))
    print("📂 Connexion à ChromaDB :", os.getenv("CHROMA_DB_PATH", "chroma_db"))

if __name__ == "__main__":
    main()
EOL
echo "🎯 Fichier main.py créé."

echo "✅ Projet initialisé avec succès !"
echo "➡️ Exécutez 'bash setup.sh' pour démarrer les services Docker."

# LangChain Demo ESN 🚀

## 📌 Objectif du Projet
Ce projet est un démonstrateur utilisant **LangChain** et **Mistral 7B via Ollama** pour assister l’analyse de documents.

## 📂 Architecture
- **Analyse de documents** : Extraction des insights et KPIs
- **Comparaison stratégique** : Alignement avec les objectifs business
- **Génération automatique de recommandations** : ROI, Impact CO₂, Roadmap

## 🛠️ Installation

### Prérequis
- **Python 3.10**
- **Docker** et **Docker Compose**
- **Git**

### Étapes d'installation

1. **Clonez le repo :**
   ```bash
   git clone https://github.com/votre-repo/langchain-demo-esn.git
   cd langchain-demo-esn
   ```

2. **Installez les dépendances Python :**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurez les variables d'environnement :**
   Créez un fichier `.env` à la racine du projet avec le contenu suivant :
   ```env
   MINIO_ACCESS_KEY=admin
   MINIO_SECRET_KEY=password
   MINIO_ENDPOINT=http://localhost:9000
   CHROMA_DB_PATH=chroma_db
   OLLAMA_MODEL=mistral
   OLLAMA_MEMORY_LIMIT=10GB
   ```

4. **Lancez les services Docker :**
   ```bash
   docker-compose up -d
   ```

5. **Initialisez le projet :**
   ```bash
   bash setup.sh
   ```

6. **Lancez le projet :**
   ```bash
   python main.py
   ```

## 🚀 Utilisation

### API
L'API est accessible à l'adresse `http://localhost:5010`. Voici quelques endpoints utiles :

- **Ajouter un document :**
  ```http
  POST /add_document/
  {
    "doc_id": "unique_document_id",
    "content": "Contenu du document",
    "metadata": {
      "author": "Auteur",
      "category": "Catégorie",
      "source": "Source"
    }
  }
  ```

- **Rechercher des documents :**
  ```http
  POST /search_documents/
  {
    "query": "Votre requête",
    "n_results": 3
  }
  ```

- **Vérifier le statut de traitement d'un document :**
  ```http
  GET /status/{doc_id}
  ```

- **Récupérer les versions d'un document :**
  ```http
  GET /document_versions/{doc_id}
  ```

### Interface Utilisateur
L'interface utilisateur est accessible à l'adresse `http://localhost:8501`.

## 🐳 Docker

### Construire et lancer les conteneurs
```bash
docker-compose up --build
```

### Arrêter les conteneurs
```bash
docker-compose down
```

## 📜 Licence
Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 📝 Auteurs
- **Stéphane MOREL** - *Initial work* - [smo-peak](https://github.com/smo-peak)

Merci d'utiliser cette Demo  ! 🚀
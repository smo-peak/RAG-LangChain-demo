# Dockerfile
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Créer la structure des dossiers
RUN mkdir -p /app/src/analysis \
    /app/src/comparison \
    /app/src/db \
    /app/src/ingestion \
    /app/src/llm \
    /app/src/reports \
    /app/src/ui

# Copier les fichiers nécessaires
COPY requirements.txt .
COPY src/main.py /app/src/
COPY src/db/chroma.py /app/src/db/
COPY src/ui/app.py /app/src/ui/
COPY src/llm/manager.py /app/src/llm/
COPY src/ingestion/document_processor.py /app/src/ingestion/

# Créer les fichiers __init__.py nécessaires
RUN touch /app/src/llm/__init__.py \
    /app/src/ingestion/__init__.py \
    /app/src/db/__init__.py

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Définir les variables d'environnement
ENV PYTHONPATH=/app

# Exposer les ports nécessaires
EXPOSE 5010 8501

# Le CMD sera remplacé par les commandes dans docker-compose.yml
CMD ["python", "src/main.py"]
#!/bin/bash

# Démarrer Ollama
ollama serve &

# Attendre que le serveur démarre
sleep 10

# Télécharger le modèle
echo "Downloading Mistral model..."
ollama pull mistral

# Garder le conteneur en vie
tail -f /dev/null
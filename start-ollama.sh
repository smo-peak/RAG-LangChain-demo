#!/bin/bash

# Démarrer Ollama en arrière-plan
ollama serve &
SERVER_PID=$!

# Attendre que le serveur soit prêt
sleep 10

# Télécharger le modèle
ollama pull mistral

# Garder le processus en vie
wait $SERVER_PID
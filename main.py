import os

def main():
    print("🚀 Bienvenue dans le démonstrateur LangChain pour ESN")
    print("🌍 Chargement du modèle :", os.getenv("OLLAMA_MODEL", "mistral"))
    print("📂 Connexion à ChromaDB :", os.getenv("CHROMA_DB_PATH", "chroma_db"))

if __name__ == "__main__":
    main()

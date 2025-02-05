# LangChain Demo with Mistral AI 🚀

## 📌 Project Objective
This project is a demonstrator using **LangChain** and **Mistral 7B via Ollama** to assist in document analysis.

## 📂 Architecture
The architecture of this project is designed to provide in-depth document analysis using advanced natural language processing (NLP) and machine learning techniques. Here are the main components:

- **Document Analysis**: Extraction of insights and KPIs from the provided documents.
- **Strategic Comparison**: Alignment of extracted information with business objectives.
- **Automatic Recommendation Generation**: Proposals for ROI, CO₂ Impact, and Roadmap based on the analyses.

### Vector Database
We use a vector database to efficiently store and search the vector representations of documents. Each document is transformed into a vector using NLP models, enabling fast and accurate semantic searches.

### Chunking
To handle large documents, we split them into smaller pieces called "chunks". Each chunk is then analyzed individually, allowing for better memory management and more detailed analysis of specific sections of the document.

## 🛠️ Installation

### Prerequisites
- **Python 3.10**
- **Docker** and **Docker Compose**
- **Git**

### Installation Steps

1. **Clone the repo:**
   ```bash
   git clone https://github.com/smo-peak/RAG-LangChain-demo.git
   cd langchain-demo-esn
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   Create a `.env` file at the root of the project with the following content:
   ```env
   MINIO_ACCESS_KEY=admin
   MINIO_SECRET_KEY=password
   MINIO_ENDPOINT=http://localhost:9000
   CHROMA_DB_PATH=chroma_db
   OLLAMA_MODEL=mistral
   OLLAMA_MEMORY_LIMIT=10GB
   ```

4. **Start Docker services:**
   ```bash
   docker-compose up -d
   ```

5. **Initialize the project:**
   ```bash
   bash setup.sh
   ```

6. **Run the project:**
   ```bash
   python main.py
   ```

## 🚀 Usage

### API
The API is accessible at `http://localhost:5010`. Here are some useful endpoints:

- **Add a document:**
  ```http
  POST /add_document/
  {
    "doc_id": "unique_document_id",
    "content": "Document content",
    "metadata": {
      "author": "Author",
      "category": "Category",
      "source": "Source"
    }
  }
  ```

- **Search documents:**
  ```http
  POST /search_documents/
  {
    "query": "Your query",
    "n_results": 3
  }
  ```

- **Check document processing status:**
  ```http
  GET /status/{doc_id}
  ```

- **Retrieve document versions:**
  ```http
  GET /document_versions/{doc_id}
  ```

### User Interface
The user interface is accessible at `http://localhost:8501`.

## 🐳 Docker

### Build and start containers
```bash
docker-compose up --build
```

### Stop containers
```bash
docker-compose down
```

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📝 Authors
- **Stéphane MOREL** - *Initial work* - [smo-peak](https://github.com/smo-peak)

Thank you for using this Demo! 🚀
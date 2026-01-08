<div align="center">

# 🤖 AI-Team

### Distributed Multi-Agent Research System with RAG Capabilities

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-FF6B35?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-DC382D?style=for-the-badge&logo=qdrant&logoColor=white)](https://qdrant.tech/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](./LICENSE)

<p align="center">
  <strong>A sophisticated multi-agent research system that emulates a professional research team structure—featuring a hierarchical "Head" coordinator and parallel "Worker" agents—to deliver comprehensive, document-grounded answers to complex queries.</strong>
</p>

---

[Features](#-features) •
[Architecture](#-architecture) •
[Installation](#-installation) •
[Usage](#-usage) •
[Configuration](#%EF%B8%8F-configuration) •
[Contributing](#-contributing)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 **Hierarchical Intelligence** | Decomposes complex queries into atomic, manageable sub-tasks for thorough investigation |
| ⚡ **High-Performance LLMs** | Powered by `gemini-2.5-flash` for optimal speed and accuracy balance |
| 🔄 **Graph-Based Workflow** | Leverages LangGraph for stateful, cyclic agent orchestration with fan-out/fan-in patterns |
| 📚 **RAG Integration** | Optional document-grounded research using Qdrant vector database for contextual answers |
| 🐳 **Docker-Ready** | One-command Qdrant deployment for seamless vector database setup |
| 📝 **Automated Aggregation** | Compiles distributed findings from worker nodes into a cohesive final report |
| 🔗 **Context Awareness** | Maintains conversation context across the entire processing pipeline |
| 🎯 **Scalable Workers** | Configurable number of parallel worker agents for customized research depth |

---

## 🏗️ Architecture

The system operates via a **directed acyclic graph (DAG)** workflow using **LangGraph**, implementing a fan-out/fan-in pattern for parallel processing:

```
                    ┌─────────────────┐
                    │   User Query    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   StartNode     │
                    │ (Lead Researcher)│
                    │  Deep Research   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  DividerNode    │
                    │(Project Manager)│
                    │  Task Division   │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ WorkerNode 1 │ │ WorkerNode 2 │ │ WorkerNode N │
    │   Research   │ │   Research   │ │   Research   │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │                │                │
           └────────────────┼────────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │   FinalNode     │
                   │  Aggregation &  │
                   │   Final Report  │
                   └─────────────────┘
```

### Node Descriptions

| Node | Role | Responsibility |
|------|------|----------------|
| **StartNode** | Lead Researcher | Analyzes user query and conducts initial broad research (with optional document context) |
| **DividerNode** | Project Manager | Breaks down broad research into JSON-structured tasks for worker distribution |
| **WorkerNode** | Research Assistant | Parallel agents executing specific sub-tasks with in-depth analysis |
| **FinalNode** | Report Compiler | Aggregates all worker outputs into a synthesized final answer |

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

| Requirement | Version | Purpose |
|-------------|---------|---------|
| [Python](https://www.python.org/downloads/) | 3.9+ | Runtime environment |
| [Docker](https://www.docker.com/get-started) | Latest | Vector database container (optional, for RAG) |
| [Google Cloud Project](https://console.cloud.google.com/) | - | Gemini API access |

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Sarthak-Jadhav-Dev/AI-Team.git
cd AI-Team
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate - Windows
.\.venv\Scripts\activate

# Activate - macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

> 💡 **Tip:** Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Document Setup (Optional - For RAG Mode)

If you want to use document-grounded research:

1. Place your PDF files in the `Place-Documents-Here/` folder
2. Ensure Docker Desktop is running
3. Select "yes" when prompted about document usage

---

## 🎮 Usage

### Basic Research Mode

```bash
python main.py
```

**Interactive Prompts:**
1. **Enter your research query:** *(e.g., "The impact of Quantum Computing on Cybersecurity")*
2. **Enter the Number of Worker Nodes:** *(e.g., `3`)*
3. **Do you want to use a document for research?:** `no`

### Document-Grounded Research Mode (RAG)

```bash
python main.py
```

**Interactive Prompts:**
1. **Enter your research query:** *(e.g., "Summarize the key findings from the research paper")*
2. **Enter the Number of Worker Nodes:** *(e.g., `3`)*
3. **Do you want to use a document for research?:** `yes`

> ⚠️ **Note:** Docker must be running for RAG mode. The system will automatically start Qdrant and process your documents.

### Example Output Flow

```
Enter your research query: Explain the applications of machine learning in healthcare
Enter the Number of Worker Nodes: 3
Do you want to use a document for research? (yes/no): no

[StartNode] Performing deep research...
[DividerNode] Distributing tasks to 3 workers...
  - Node1: "Diagnostic AI Systems"
  - Node2: "Drug Discovery & Development"  
  - Node3: "Patient Care & Monitoring"
[WorkerNodes] Parallel execution...
[FinalNode] Aggregating final report...
```

---

## 📂 Project Structure

```
AI-Team/
│
├── 📄 main.py                    # Entry point & LangGraph definition
├── 📄 documentLoader.py          # PDF processing & vector store creation
├── 📄 docker-compose.yml         # Qdrant vector database container
├── 📄 requirements.txt           # Python dependencies
├── 📄 .env                       # Environment variables (secret)
├── 📄 .gitignore                 # Git ignore rules
├── 📁 Place-Documents-Here/      # Drop PDFs here for RAG mode
│   └── 📄 *.pdf                  # Your research documents
└── 📄 README.md                  # Documentation
```

---

## 🔧 Technical Stack

<div align="center">

| Category | Technology |
|----------|------------|
| **LLM Framework** | LangChain, LangGraph |
| **AI Model** | Google Gemini 2.5 Flash |
| **Embeddings** | Google Generative AI Embeddings |
| **Vector Store** | Qdrant (Docker) |
| **Document Processing** | PyPDF, LangChain Document Loaders |
| **Text Splitting** | RecursiveCharacterTextSplitter |

</div>

---

## 🛣️ Roadmap

- [ ] Web UI interface for easier interaction
- [ ] Support for multiple document formats (DOCX, TXT, MD)
- [ ] Streaming responses for real-time output
- [ ] Export reports to PDF/Markdown
- [ ] Memory persistence across sessions
- [ ] API endpoint for programmatic access

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. **Fork** the Project
2. **Create** your Feature Branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit** your Changes
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push** to the Branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open** a Pull Request

---

## 🐛 Troubleshooting

<details>
<summary><strong>Docker-related Issues</strong></summary>

- Ensure Docker Desktop is running before using RAG mode
- Check if port `6333` is available (Qdrant default port)
- Run `docker-compose down` to reset the container if needed

</details>

<details>
<summary><strong>API Key Issues</strong></summary>

- Verify your API key is correctly set in the `.env` file
- Ensure there are no extra spaces or quotes around the key
- Check if your Google Cloud project has the Gemini API enabled

</details>

<details>
<summary><strong>Document Processing Issues</strong></summary>

- Ensure PDFs are placed in the `Place-Documents-Here/` folder
- Check if PDFs are not password-protected or corrupted
- Verify sufficient disk space for vector embeddings

</details>

---

## 📄 License

This project is distributed under the **MIT License**. See `LICENSE` for more information.

---

## 👤 Author

**Sarthak Jadhav**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Sarthak-Jadhav-Dev)

---

<div align="center">

### ⭐ Star this repo if you find it helpful!

Made with ❤️ using LangGraph & Google Gemini

</div>

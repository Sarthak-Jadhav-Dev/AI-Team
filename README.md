# 🤖 AI-Team: Distributed Research Agent Swarm

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-orange)](https://langchain-ai.github.io/langgraph/)
[![Gemini](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-8E75B2)](https://deepmind.google/technologies/gemini/)

**AI-Team** is a sophisticated multi-agent research system built with **LangGraph** and **Google Gemini**. It emulates a professional research team structure—with a "Head" node acting as a coordinator and multiple "Worker" nodes executing specialized sub-tasks—to deliver comprehensive answers to complex user queries.

---

## 🚀 Features

- **🧠 Hierarchical Intelligence**: Decomposes complex queries into atomic sub-tasks.
- **⚡ High-Performance LLMs**: Powered by `gemini-2.5-flash` for speed and accuracy.
- **🔄 Graph-Based Workflow**: Utilizes LangGraph for stateful, cyclic agent orchestration.
- **🔗 Context Awareness**: Maintains context across the "Head" (Planner) and "Worker" (Executor) nodes.
- **📝 Automated Aggregation**: Compiles distributed findings into a single, cohesive final report.

---

## 🛠️ Architecture

The system operates via a directed graph workflow:

1.  **StartNode**: The "Lead Researcher" analyzes the user query and conducts initial broad research.
2.  **DividerNode**: Acts as a Project Manager, breaking down the broad research into valid JSON tasks for the team.
3.  **WorkerNode**: Parallel autonomous agents ensuring specific sub-tasks are answered concisely.
4.  **FinalNode**: Aggregates all worker outputs into a final synthesized answer.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- [Python 3.9+](https://www.python.org/downloads/)
- A [Google Cloud Project](https://console.cloud.google.com/) with Gemini API enabled.

---

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Sarthak-Jadhav-Dev/AI-Team.git
    cd AI-Team
    ```

2.  **Create a virtual environment (Optional but Recommended)**
    ```bash
    python -m venv .venv
    # Windows
    .\.venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

## ⚙️ Configuration

1.  Create a `.env` file in the root directory.
2.  Add your Google Gemini API key:

    ```env
    GOOGLE_API_KEY=your_actual_api_key_here
    ```

---

## 🎮 Usage

Run the main application entry point:

```bash
python main.py
```

Follow the interactive prompts:
1.  **Enter your research query**: (e.g., *"The impact of Quantum Computing on Cybersecurity"*)
2.  **Enter the Number of Worker Nodes**: (e.g., `3`)

The agents will start processing, showing output for the Deep Research phase, Task Distribution, and Final Aggregation.

---

## 📂 Project Structure

```bash
AI-Team/
├── .venv/                 # Virtual environment
├── main.py                # Entry point & Graph definition
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (secret)
└── README.md              # Documentation
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

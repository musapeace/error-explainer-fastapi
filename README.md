# 🤖 Error Explainer Agent

The **Error Explainer Agent** is a specialized AI-powered assistant built on **Python/FastAPI** that integrates with **Telex.im** via the **A2A Protocol** to solve a real-world developer problem. Its main function is to analyze obscure technical error messages (from Python, Linux, or general systems) and translate them into clear, actionable solutions.

---

## 🎯 Agent Goal and Output Structure

The agent uses a strict system prompt to ensure consistency and immediate utility. When a user submits an error, the response will contain three mandatory sections:

1.  **Simple Explanation:** A non-technical meaning of the error.
2.  **Likely Cause:** The single most probable source of the problem.
3.  **Suggested Fixes:** 1–3 clear, numbered steps to resolve the issue.

---

## 🛠️ Technology Overview

| Component | Technology | Role in Project |
| :--- | :--- | :--- |
| **Backend Framework** | **Python (FastAPI)** | High-performance API server. |
| **AI Engine** | **Google Gemini** | Provides the reasoning and content generation. |
| **Protocol** | **A2A (JSON-RPC 2.0)** | Standardized communication interface for Telex.im. |
| **Tooling** | **Pydantic** | Validates the complex nested A2A JSON data structure. |
| **Deployment Target** | **Railway / Docker** | Ensures a consistent, reliable production environment. |

---

## ⚙️ Development Guide

### 1. Local Setup Instructions

1.  **Clone & Setup Venv:**
    ```bash
    # Clone your repo first
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
2.  **Configure Key:** Create a **`.env`** file in the root directory with your key:
    ```text
    # .env
    GEMINI_API_KEY="[YOUR_LIVE_GEMINI_KEY_HERE]"
    ```
3.  **Run Locally:**
    ```bash
    # Note: 'app.main:app' targets the main.py file inside the app/ directory
    (venv) $ python3 -m uvicorn app.main:app --reload
    ```
    The local endpoint will be `http://127.0.0.1:8000/a2a/explain`.

### 2. Deployment Setup

The application is configured with a `Procfile` and `Dockerfile` in the root for seamless deployment to Railway.

---


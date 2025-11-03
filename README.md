# 🧠 Error Explainer Agent

## 🚀 Overview
The **Error Explainer Agent** explains technical error messages (like Python, Linux, or system errors) in simple, clear language.  
It connects to **Telex.im** and automatically replies when users post an error message.

---

## 🧩 Features
- Accepts JSON-RPC requests from Telex.im  
- Extracts error messages and explains them  
- Built with FastAPI  
- Easy to deploy using ngrok or Railway  

---

## 🏗️ Tech Stack
- Python 3.10+  
- FastAPI  
- Pydantic  
- Uvicorn  

---

## 📦 Installation

```bash
git clone https://github.com/musapeace/error-explainer-agent.git
cd error-explainer-agent
pip install -r requirements.txt
uvicorn main:app --reload

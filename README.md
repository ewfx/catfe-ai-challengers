# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---
## 🎯 Introduction
The Context-Aware AI-Driven Testing System is an advanced, multi-agent AI-powered framework designed to automate financial test generation, execution, fraud detection, and compliance validation. This system leverages Generative AI with LLM’s, NLP, and ML models to create dynamic test cases from various financial data sources, ensuring optimal accuracy, security, and efficiency in financial transactions.
## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)

## 💡 Inspiration
Traditional test case generation is time-consuming, costly, and prone to human error. Testers struggle to create real-world financial transaction test scenarios covering fraud detection, regulatory compliance, and
risk assessment. Financial institutions maintain millions of test cases, many of which become obsolete or redundant over time. Manual updates to test cases are not scalable and result in poor test coverage when
system changes occur.
Frequent updates to AML (Anti-Money Laundering), GDPR, PCI-DSS, SOX, and other compliance frameworks make manual compliance testing inefficient. Banking operations, fund transfers, KYC validation, and credit risk assessments involve multiple transaction layers that require end-to-end testing. Rapid changes in pricing algorithms, fraud detection mechanisms, and AI-driven financial decision-making introduce new test case requirements. Manual compliance testing fails to detect violations proactively.

## ⚙️ What It Does
Connects to various sources, gnerates the test cases, updates the test cases, generates the automation scripts and executes the tests 
## 🛠️ How We Built It
Briefly outline the technologies, frameworks, and tools used in development.

## 🚧 Challenges We Faced
Describe the major technical or non-technical challenges your team encountered.

## 🏃 How to Run
1. Clone the repository:
```bash
git clone https://github.com/catefe-ai-challengers/GenAI_TestingSystem.git
```

2. Install backend dependencies:
```bash
cd GenAI_TestingSystem
pip install -r requirements.txt
```

3. ../ai_automation_platform
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

4. Run the client app:
```bash
cd GenAI_TestingSystem/clientapp/build
python -m http.server 4200
open url http://localhost:4200/genAI-testing-system/ in browser
```


## 🏗️ Tech Stack
**Frontend (UI):** ReactJS Backend (APIs): FastAPI Data Processing: MongoDB, FAISS
**AI & ML:** LangChain, AutoGen, Hugging Face, Llamma, OpenAI, Claude TensorFlow, NLP
**Automation & Testing:** Cucumber, SpecFlow

## 👥 Team
-  Nagarjuna Madupu
-  Sunirmal Sikder
-  Ram Polagani
-  Eswar Lanka

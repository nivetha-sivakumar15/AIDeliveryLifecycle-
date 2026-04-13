# AIDeliveryLifecycle
AI-powered SDLC automation tool that converts business inputs into user stories, TDDs, and test scenarios for faster delivery lifecycle execution.

🎯 Use Case
In a typical delivery lifecycle, teams manually convert:

Meeting transcripts
Process flows

into:

User stories
Design documents
Test cases


🧩 Features
Generate Epics, User Stories & Acceptance Criteria
Convert outputs into Jira-ready CSV format
Generate Technical Design Documents (TDD)
Generate Unit Test Scenarios (>90% coverage)
Generate End-to-End Test Scenarios (>70% coverage)

🛠️ Tech Stack
Python
AI API (Gemini / LLM-based)
VS Code

📂 Project Structure
ai_sdlc_generator/
│
├── inputs/
├── outputs/
├── src/
│   ├── story_generator.py
│   ├── tdd_generator.py
│   ├── test_generator.py
│   ├── e2e_generator.py
│   ├── jira_formatter.py
│   └── input_parser.py
│
└── main.py

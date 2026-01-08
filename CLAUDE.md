# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

**ExamTutor** - An AI-powered learning platform for UK students preparing for 11+ entrance exams and GCSEs. Built on the architecture of DeepTutor/AIEducator.

## Architecture

- **Backend**: Python 3.12+, FastAPI (port 8001)
- **Frontend**: Next.js, React, TailwindCSS (port 3782)
- **RAG Engine**: LightRAG for knowledge graph-based retrieval
- **LLM Support**: OpenAI, Ollama, LM Studio
- **Content API**: Oak National Academy (Open Government License)

### Key Directories

```
src/
├── api/            # FastAPI backend endpoints
├── agents/         # AI agent implementations (explain, practice, mock_exam)
├── knowledge/      # RAG and curriculum knowledge base
├── question_bank/  # Question storage and retrieval
├── progress/       # Student progress tracking
├── tools/          # Tools for agents
└── core/           # Core utilities and configuration

web/
├── app/            # Next.js app router pages
├── components/     # React components
├── context/        # React context providers
└── lib/            # Utility functions

data/
├── curriculum/     # National curriculum documents
├── questions/      # Question bank data
└── oak_content/    # Cached Oak Academy content

config/
├── main.yaml       # Server configuration
├── agents.yaml     # Agent configurations
└── exams.yaml      # Exam board specifications
```

## Development Commands

### Setup
```bash
# Create Python virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd web && npm install
```

### Running
```bash
source venv/bin/activate
python scripts/start_web.py

# Frontend: http://localhost:3782
# Backend: http://localhost:8001/docs
```

### Testing
```bash
pytest tests/
cd web && npm run lint
```

## Key APIs

### Oak National Academy
- Base URL: https://open-api.thenational.academy/
- License: Open Government License
- Used for: Curriculum-aligned lessons, videos, quizzes

### Exam Board Past Papers
- Link to official sources, don't host
- AQA: https://www.aqa.org.uk/find-past-papers-and-mark-schemes
- Edexcel: https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html

## Content Strategy

1. **Primary**: Oak API content (free, legal)
2. **Secondary**: AI-generated questions based on patterns
3. **Tertiary**: Links to official exam board resources

## Exam Types Supported

### 11+ (Year 5-6, ages 10-11)
- GL Assessment (most common)
- CEM (Durham University)
- Subjects: Verbal Reasoning, Non-Verbal Reasoning, Maths, English

### GCSEs (Year 10-11, ages 14-16)
- AQA, Edexcel, OCR, WJEC
- Core: English, Maths, Science
- Options: History, Geography, Languages, etc.

## Key Files

- `PLAN.md` - Comprehensive project plan and research
- `settings.py` - Pydantic settings for configuration
- `config/exams.yaml` - Exam specifications and question types

# ExamTutor

AI-powered learning platform for UK 11+ and GCSE exam preparation.

## Features

- **11+ Preparation**: Verbal Reasoning, Non-Verbal Reasoning, Maths, English
- **GCSE Revision**: All major subjects across AQA, Edexcel, OCR boards
- **Adaptive Learning**: Personalized difficulty based on performance
- **AI Tutoring**: Explain concepts, work through problems, identify weaknesses
- **Mock Exams**: Timed practice under exam conditions
- **Progress Tracking**: Topic mastery, predicted grades, revision plans

## Quick Start

```bash
# Clone and setup
git clone <repo-url>
cd ExamTutor

# Python environment
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd web && npm install && cd ..

# Run
python scripts/start_web.py
```

Visit http://localhost:3782

## Architecture

Built on the DeepTutor framework:
- **Backend**: FastAPI (Python 3.12+)
- **Frontend**: Next.js + React + TailwindCSS
- **Knowledge**: LightRAG for curriculum understanding
- **Content**: Oak National Academy API (Open Government License)

## Content Sources

| Source | License | Content |
|--------|---------|---------|
| [Oak National Academy](https://open-api.thenational.academy/) | OGL | Lessons, quizzes, videos |
| [National Curriculum](https://www.gov.uk/government/collections/national-curriculum) | Crown Copyright | Curriculum frameworks |
| Exam Boards | Educational use | Past papers (linked) |
| AI Generated | Original | Practice questions |

## Exam Coverage

### 11+ Exams
- GL Assessment format (70% of grammar schools)
- CEM format
- 21 Verbal Reasoning question types
- All Non-Verbal Reasoning patterns

### GCSEs
- AQA, Edexcel, OCR specifications
- Core subjects: English, Maths, Science
- Full mark scheme alignment

## Development

See [PLAN.md](./PLAN.md) for detailed architecture and roadmap.

```bash
# Run tests
pytest tests/

# Frontend lint
cd web && npm run lint
```

## License

MIT

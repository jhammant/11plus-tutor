# 11+ Tutor

Free, open-source AI-powered 11+ exam preparation for grammar school entrance.

## Features (Opensource - Free)

- **Practice Questions**: 239+ questions across verbal reasoning, maths, and more
- **Mock Exams**: Full GL-style timed practice exams
- **Progress Tracking**: Track your accuracy and improvement over time
- **Achievements**: Gamification with badges and streaks
- **Local LLM Support**: Run with Ollama or LM Studio for complete privacy

## Paid Features (Coming Soon)

- **AI Tutor**: Get explanations and hints from an AI tutor
- **Question Generation**: Unlimited AI-generated practice questions
- **Advanced Analytics**: Predicted grades, detailed weakness analysis
- **Adaptive Difficulty**: Questions that adjust to your level
- **Parent Dashboard**: Multi-child tracking and reports
- **Cloud Sync**: Access your progress from any device

## Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/elevenplustutor
cd elevenplustutor

# Python environment
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd web && npm install && cd ..

# Run
python scripts/start_app.py
```

Visit http://localhost:3783

## Architecture

- **Backend**: FastAPI (Python 3.12+)
- **Frontend**: Next.js 16 + React 19 + TailwindCSS
- **Database**: SQLite (local)
- **LLM**: Ollama / LM Studio (local) or OpenAI (paid)

## 11+ Exam Coverage

### GL Assessment (70% of grammar schools)
- **Verbal Reasoning**: Synonyms, antonyms, analogies, code words, letter sequences, odd one out
- **Non-Verbal Reasoning**: Patterns, matrices, rotations (coming soon)
- **Mathematics**: Arithmetic, fractions, sequences, word problems
- **English**: Comprehension, vocabulary (coming soon)

### CEM (Durham University)
- Integrated papers with rapid section changes
- Broader vocabulary focus

## Configuration

### Opensource Mode (Default)
Uses local LLM for privacy. Set up Ollama or LM Studio:

```bash
# .env
APP_MODE=opensource
LLM_BINDING=ollama
LLM_HOST=http://localhost:11434/v1/
LLM_MODEL=llama3.2
```

### Paid Mode
For cloud-based AI features:

```bash
# .env
APP_MODE=paid
LLM_BINDING=openai
LLM_HOST=https://api.openai.com/v1
LLM_MODEL=gpt-4o
LLM_API_KEY=sk-your-key
```

## Development

```bash
# Run tests
pytest tests/

# Frontend lint
cd web && npm run lint

# Generate more questions
python scripts/generate_questions.py --subject verbal_reasoning --type synonyms --count 50
```

## Content Sources

| Source | License | Content |
|--------|---------|---------|
| AI Generated | Original | Practice questions |
| [Oak National Academy](https://open-api.thenational.academy/) | OGL | Curriculum alignment |

## License

MIT - Free to use, modify, and distribute.

## Contributing

Contributions welcome! Please see CONTRIBUTING.md for guidelines.

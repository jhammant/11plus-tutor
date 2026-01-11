# 11+ Tutor

**Free, open-source 11+ exam preparation to help your child get into grammar school.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-green.svg)
![Questions](https://img.shields.io/badge/questions-1364-brightgreen.svg)
![Tests](https://img.shields.io/badge/tests-57%20passing-success.svg)

## Why This Exists

11+ tutoring costs £40-80/hour. Practice books cost £10-15 each and run out quickly. Many families can't afford proper preparation, putting their children at a disadvantage.

**This tool is free, unlimited, and runs entirely on your computer.**

---

## What's Included

### 1,364 Verified Questions

| Subject | Questions | Coverage |
|---------|-----------|----------|
| **Verbal Reasoning** | 523 | Synonyms, antonyms, analogies, letter sequences, code words, odd one out, hidden words, compound words |
| **Mathematics** | 366 | Number sequences, arithmetic, fractions |
| **Non-Verbal Reasoning** | 300 | Pattern sequences, shape analogies, odd one out (all with SVG graphics) |
| **English** | 175 | Reading comprehension (Aesop's Fables), spelling, grammar |

### Question Quality
- **Programmatic questions** are mathematically verified (sequences, arithmetic)
- **Word-based questions** validated against curated word lists
- **All questions** pass automated testing before release
- **Wrong answer?** Report it and we'll fix it immediately

### Learning Features
- **Topic Lessons** - Understand concepts before practicing
- **Strategy Guides** - Step-by-step approaches for each question type
- **Worked Examples** - Detailed explanations for every answer
- **Mock Exams** - Timed practice under exam conditions

---

## Quick Start

### One-Line Install (Recommended)

**Mac / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/11plus-tutor/main/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/yourusername/11plus-tutor/main/scripts/install.ps1 | iex
```

The installer will:
- ✅ Check for Python & Node.js (help you install if missing)
- ✅ Download 11+ Tutor
- ✅ Set up everything automatically
- ✅ Create a simple `start.sh` or `start.bat` to launch anytime

**No LLM required!** All 1,364 questions work immediately.

---

### Manual Install (Alternative)

If you prefer to install manually:

```bash
# 1. Download the code
git clone https://github.com/yourusername/11plus-tutor.git
cd 11plus-tutor

# 2. Set up Python
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Set up the website
cd web && npm install && cd ..

# 4. Start the app
python scripts/start_app.py
```

Open http://localhost:3783 in your browser. That's it!

---

## LLM Setup Options

### Do I Need an LLM?

**No!** The app works perfectly without any LLM. All 1,364 questions are pre-generated and stored in the database.

| Feature | Without LLM | With LLM |
|---------|------------|----------|
| Practice all questions | ✅ | ✅ |
| Mock exams with timer | ✅ | ✅ |
| Progress tracking | ✅ | ✅ |
| Strategy guides | ✅ | ✅ |
| Achievements & streaks | ✅ | ✅ |
| Printable worksheets | ✅ | ✅ |
| AI Tutor chat | ❌ | ✅ |
| "Explain this answer" | ❌ | ✅ |
| Generate new questions | ❌ | ✅ |

**Recommendation:** Start without an LLM. Add one later if you want AI explanations.

### Option 1: No LLM (Recommended for Most Users)

Just run the app! Everything works out of the box.

```bash
python scripts/start_app.py
```

### Option 2: Local LLM (Privacy-Focused)

Run AI on your own computer. Requires 8GB+ RAM.

**Using LM Studio (Easiest):**
1. Download [LM Studio](https://lmstudio.ai/) (free)
2. Download a model (search "llama 3.2" or "mistral")
3. Click "Start Server" (default port 1234)
4. Create `.env` file:
```bash
LLM_BINDING=openai
LLM_HOST=http://localhost:1234/v1
LLM_MODEL=local-model
LLM_API_KEY=lm-studio
```
5. Restart the app

**Using Ollama:**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh  # Mac/Linux
# Windows: download from ollama.ai

# Get a model (3B is light, 8B is smarter)
ollama pull llama3.2      # 3B model, works on most machines
# OR
ollama pull llama3.1:8b   # 8B model, needs 16GB RAM

# Create .env file
LLM_BINDING=ollama
LLM_HOST=http://localhost:11434/v1/
LLM_MODEL=llama3.2
LLM_API_KEY=ollama
```

### Option 3: Cloud LLM (Low-Spec Machines)

Use OpenAI, Anthropic, or other cloud providers. Costs ~$0.01-0.05 per AI interaction.

**OpenAI:**
```bash
# Create .env file
LLM_BINDING=openai
LLM_HOST=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
LLM_API_KEY=sk-your-api-key-here
```

**Anthropic Claude:**
```bash
# Create .env file
LLM_BINDING=openai
LLM_HOST=https://api.anthropic.com/v1
LLM_MODEL=claude-3-haiku-20240307
LLM_API_KEY=sk-ant-your-api-key-here
```

**Groq (Free Tier Available):**
```bash
# Create .env file
LLM_BINDING=openai
LLM_HOST=https://api.groq.com/openai/v1
LLM_MODEL=llama-3.1-8b-instant
LLM_API_KEY=gsk_your-api-key-here
```

### Quick Comparison

| Option | Cost | Speed | Privacy | Requires |
|--------|------|-------|---------|----------|
| No LLM | Free | N/A | Perfect | Nothing |
| LM Studio | Free | Varies | Perfect | 8GB+ RAM |
| Ollama | Free | Varies | Perfect | 8GB+ RAM |
| OpenAI | ~$0.01/use | Fast | Data sent | API key |
| Groq | Free tier | Very fast | Data sent | API key |

---

## For Parents: How to Use This

### Daily Practice Routine (20-30 minutes)
1. **Learn** (5 min) - Read the topic lesson for one question type
2. **Strategy** (5 min) - Review the strategy guide with your child
3. **Practice** (15 min) - Do 10-15 questions with instant feedback
4. **Review** (5 min) - Go over any wrong answers together

### Weekly Mock Exam
- Use the Mock Exam feature for timed practice
- Simulates real exam pressure
- Identifies weak areas to focus on

### Track Progress
- The app tracks questions attempted and accuracy
- Focus on question types with lower scores
- Aim for 80%+ accuracy before moving on

---

## Question Types Explained

### Verbal Reasoning (VR)
| Type | Example | What It Tests |
|------|---------|---------------|
| Synonyms | happy = joyful | Vocabulary |
| Antonyms | hot ≠ cold | Vocabulary |
| Analogies | cat:kitten :: dog:? | Relationships |
| Letter Sequences | AB, CD, EF, ? | Pattern recognition |
| Hidden Words | COST + AGE = STAGE | Word finding |
| Compound Words | SUN + FLOWER = ? | Word building |

### Non-Verbal Reasoning (NVR)
| Type | What It Tests |
|------|---------------|
| Pattern Sequences | Shape rotation, size changes |
| Shape Analogies | "A is to B as C is to ?" |
| Odd One Out | Which shape doesn't belong |

### Mathematics
| Type | Topics |
|------|--------|
| Number Sequences | Arithmetic, quadratic patterns |
| Arithmetic | Addition, subtraction, multiplication, division |
| Fractions | Basic fraction operations |

### English
| Type | Content |
|------|---------|
| Comprehension | Aesop's Fables with questions |
| Spelling | Commonly misspelled words |
| Grammar | Fill-in-the-blank sentences |

---

## Generating More Questions

Need more practice? Generate unlimited questions:

```bash
source venv/bin/activate

# Generate 100 more math sequences
python scripts/generate_questions.py --type sequences --count 100

# Generate 50 more NVR questions
python scripts/generate_nvr.py --type all --count 50

# Generate more VR questions
python scripts/generate_vr_expanded.py --count 100

# Validate all questions
python scripts/validate_questions.py
```

---

## Contributing

**Every contribution helps a child.** See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Quick Wins (No Coding Required)
- **Report wrong answers** - Open an issue with the question ID
- **Add word pairs** - Expand synonym/antonym lists
- **Suggest passages** - Find public domain text for comprehension

### Code Contributions
- **Add question types** - CEM format, more NVR types
- **Improve UI** - Mobile responsiveness, accessibility
- **Add features** - Printable worksheets, progress export

### Run Tests Before Submitting
```bash
python scripts/test_harness.py  # Should show 57/57 passing
```

---

## What's Missing (Help Wanted!)

### Question Types We Need
- [ ] CEM-style questions (different from GL Assessment)
- [ ] Cube nets (which cube from this net?)
- [ ] Paper folding (punch and unfold)
- [ ] 3D rotation
- [ ] Cloze passages (fill in blanks)
- [ ] Shuffled sentences

### Features We Need
- [ ] Docker for one-command setup
- [ ] Printable worksheet generator
- [ ] Mobile app (React Native?)
- [ ] Spaced repetition scheduling
- [ ] Parent dashboard with reports

---

## Exam Boards Covered

| Board | Status | Notes |
|-------|--------|-------|
| **GL Assessment** | Good | Most question types covered |
| **CEM** | Partial | Need more cloze/comprehension |
| **ISEB** | Partial | Similar to GL |

Different regions use different tests. Check which board your target schools use.

---

## FAQ

**Q: Is this as good as a tutor?**
A: No substitute for a good tutor, but this provides unlimited free practice. Many families use both.

**Q: Are the answers definitely correct?**
A: Programmatic questions (maths, sequences) are computed and guaranteed correct. Word-based questions are validated against curated lists. Report any errors immediately.

**Q: My child is struggling with [X]. What should I do?**
A: Focus on that topic using the filters. Read the strategy guide together. Do 10 questions, review wrong answers, repeat.

**Q: Can I use this offline?**
A: Yes, once installed everything runs locally. No internet needed.

**Q: Is my child's data sent anywhere?**
A: No. Everything stays on your computer. We don't collect any data.

---

## License

MIT License - free for everyone, forever.

---

## Acknowledgments

- Built with [Next.js](https://nextjs.org/), [FastAPI](https://fastapi.tiangolo.com/), [Tailwind CSS](https://tailwindcss.com/)
- AI features via [LM Studio](https://lmstudio.ai/) or [Ollama](https://ollama.ai/)
- Comprehension passages from Aesop's Fables (public domain)

---

**Made with love to help every child have a fair chance at grammar school.**

*If this helped your child, consider starring the repo and sharing with other parents.*

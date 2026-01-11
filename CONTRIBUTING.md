# Contributing to 11+ Tutor

Thank you for wanting to help kids succeed in their 11+ exams! This guide will help you contribute effectively.

## Quick Ways to Help

### 1. Report Wrong Answers (5 minutes)
Found a question with a wrong answer? This is **critical** - wrong answers are worse than no tool at all.

1. Note the question ID (shown in browser console or URL)
2. Open an issue with:
   - Question ID
   - The wrong answer shown
   - What the correct answer should be
   - Your reasoning

### 2. Add Word Pairs (15 minutes)
Expand our synonym/antonym validation in `scripts/validate_questions.py`:

```python
# Add to SYNONYM_PAIRS
('your_word', 'synonym'),

# Add to ANTONYM_PAIRS
('word1', 'opposite'),
```

### 3. Add Comprehension Passages (30 minutes)
Add public domain passages to `scripts/generate_english.py`:

**Good sources for public domain text:**
- Aesop's Fables (we use these)
- Grimm's Fairy Tales
- Public domain children's literature
- Wikipedia (CC licensed)

**Requirements:**
- Age-appropriate (10-11 year olds)
- 150-300 words ideal
- Clear moral or main idea
- 5 comprehension questions per passage

### 4. Add NVR Patterns (1 hour)
Extend `scripts/generate_nvr.py` with new pattern types:
- Reflection patterns
- Color change sequences
- Multiple attribute changes
- More complex rotations

---

## Development Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/11plus-tutor.git
cd 11plus-tutor

# Python setup (3.12 recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend setup
cd web && npm install && cd ..

# Run the app
python scripts/start_app.py

# Run tests
python scripts/test_harness.py
python scripts/validate_questions.py
```

---

## Question Generation

### Programmatic Questions (Preferred)
Questions where answers are **computed** are guaranteed correct:

```python
# Example: Number sequence
def generate_sequence():
    start = random.randint(1, 20)
    diff = random.randint(2, 7)
    sequence = [start + i * diff for i in range(4)]
    answer = sequence[-1] + diff  # Computed, guaranteed correct
    return sequence, answer
```

### Word-Based Questions (Needs Validation)
Questions using word lists need validation:

```python
# Add words to SYNONYM_PAIRS in validate_questions.py
SYNONYM_PAIRS = {
    ('happy', 'joyful'),  # Verified pair
    # ... add more
}
```

### Manual Questions (Needs Review)
Complex questions need human review before merging.

---

## Code Style

- Python: Follow PEP 8
- TypeScript: ESLint + Prettier
- Commits: Conventional commits (`feat:`, `fix:`, `docs:`)
- PRs: Include test results from `test_harness.py`

---

## Testing Your Changes

Before submitting a PR:

```bash
# 1. Run the test harness
python scripts/test_harness.py
# Expected: 57/57 passed

# 2. Validate questions
python scripts/validate_questions.py
# Check for any new issues

# 3. Test in browser
python scripts/start_app.py
# Try your new questions manually
```

---

## What We Need Most

### High Priority
- [ ] More NVR pattern types (cube nets, paper folding)
- [ ] CEM-style questions (different from GL Assessment)
- [ ] More comprehension passages
- [ ] Mobile-responsive improvements
- [ ] Docker setup for easy deployment

### Medium Priority
- [ ] Printable worksheet generator
- [ ] Progress export for parents
- [ ] Timed mock exam mode improvements
- [ ] Spaced repetition algorithm

### Nice to Have
- [ ] Audio for younger kids
- [ ] Multiple language support
- [ ] Raspberry Pi deployment guide
- [ ] Browser extension for quick practice

---

## Question Types We're Missing

### GL Assessment (21 VR Types)
We have most, but missing:
- [ ] Move a letter
- [ ] Word-number codes
- [ ] Number series (letter=number)
- [ ] Alphabet position questions

### CEM Style
CEM tests are different from GL:
- [ ] Cloze passages (fill in blanks in text)
- [ ] Shuffled sentences
- [ ] Extended comprehension
- [ ] Verbal reasoning within passages

### More NVR
- [ ] Cube nets (which cube from this net?)
- [ ] Paper folding (punch hole, unfold)
- [ ] Hidden shapes (find shape in complex figure)
- [ ] 3D rotation
- [ ] Matrices (3x3 grid patterns)

---

## Recognition

Contributors will be added to README.md and the app's About page.

Thank you for helping kids succeed! 🎓

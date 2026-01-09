# ExamTutor Roadmap - Making It Amazing

## Current State
- 17 questions (VR + Maths)
- Basic practice mode with instant feedback
- Clean exam-focused UI
- API with progress tracking

---

## Priority 1: Core Experience (This Week)

### 1.1 More Questions - CRITICAL
**Problem:** Only 17 questions isn't enough for real practice
**Solution:** Generate 500+ questions across all types

```bash
# Generate batch of questions
python scripts/generate_questions.py --subject verbal_reasoning --type synonyms --count 50
python scripts/generate_questions.py --subject verbal_reasoning --type antonyms --count 50
python scripts/generate_questions.py --subject verbal_reasoning --type analogies --count 50
python scripts/generate_questions.py --subject verbal_reasoning --type odd_one_out --count 50
python scripts/generate_questions.py --subject verbal_reasoning --type code_words --count 50
python scripts/generate_questions.py --subject mathematics --type arithmetic --count 50
python scripts/generate_questions.py --subject mathematics --type fractions --count 50
python scripts/generate_questions.py --subject mathematics --type sequences --count 50
```

### 1.2 Timed Practice Mode
**Why:** Real 11+ exams are timed - students need to practice under pressure
**Features:**
- Configurable timer (45 mins default)
- Question counter
- Submit when time runs out
- Performance report at end

### 1.3 Progress Dashboard
**Why:** Students/parents need to see improvement
**Features:**
- Overall accuracy over time (chart)
- Questions practiced per day
- Strength/weakness by topic
- Streak calendar
- Predicted exam score

### 1.4 Difficulty Levels
**Why:** Questions should adapt to student ability
**Features:**
- Foundation (easy) → Challenge (hard)
- Filter by difficulty
- Adaptive: harder after correct, easier after wrong

---

## Priority 2: Engagement (Next 2 Weeks)

### 2.1 Achievements & Gamification
- First Question, First 10, First 100
- Perfect Score (all correct in a session)
- Speed Demon (finish under time)
- Streak Master (7 days, 30 days)
- Subject Expert badges
- XP points for questions answered

### 2.2 Daily Goals
- Set daily question target (default: 20)
- Progress bar through the day
- Celebration on completion
- Streak bonus for consecutive days

### 2.3 Mock Exams
- Full GL-style mock papers
- 80 questions, 45 minutes
- Realistic exam conditions
- Detailed results breakdown
- Compare to previous attempts

### 2.4 Weak Area Focus
- Identify topics with <70% accuracy
- Suggest focused practice sessions
- "You need more practice on: Code Words"
- One-click drill mode

---

## Priority 3: Content Quality (Ongoing)

### 3.1 Question Review System
- Flag poor questions
- Rate question quality (thumbs up/down)
- Admin review queue
- Auto-retire low-rated questions

### 3.2 Detailed Explanations
- Step-by-step worked solutions
- "Why wrong" for each incorrect option
- Related concept links
- Video explanations (future)

### 3.3 Difficulty Calibration
- Track success rate per question
- Auto-adjust difficulty rating
- Remove questions that are always wrong (likely errors)

---

## Priority 4: Parent/Teacher Features (Month 2)

### 4.1 Parent Dashboard
- Child's progress summary
- Weekly email reports
- Compare to target/benchmark
- Recommended focus areas

### 4.2 Multiple Profiles
- Support for siblings
- Switch between children
- Individual progress tracking

### 4.3 Export & Reports
- PDF progress reports
- Print mock exam results
- Share achievements

---

## Priority 5: Advanced Features (Month 3+)

### 5.1 AI Tutor Chat
- Ask questions about topics
- Get explanations on demand
- "Explain this concept to me"
- Socratic teaching method

### 5.2 Non-Verbal Reasoning
- Image-based questions
- Pattern recognition
- Requires image generation/curation

### 5.3 English Comprehension
- Passage-based questions
- Multiple questions per passage
- Vocabulary in context

### 5.4 GCSE Expansion
- AQA/Edexcel specifications
- Subject-specific content
- Mark scheme alignment
- Past paper integration

---

## Technical Improvements

### Performance
- [ ] Question pre-loading
- [ ] Offline support (PWA)
- [ ] Mobile app (React Native)

### Analytics
- [ ] Mixpanel/Amplitude integration
- [ ] Learning analytics
- [ ] A/B testing framework

### Infrastructure
- [ ] PostgreSQL for scale
- [ ] Redis for caching
- [ ] CDN for assets
- [ ] Deployment to Vercel/Railway

---

## Quick Wins (Do Today)

1. **Generate 200 more questions** - 30 mins
2. **Add timer to practice page** - 1 hour
3. **Create progress page** - 2 hours
4. **Add streak tracking** - 1 hour
5. **Mobile-friendly adjustments** - 1 hour

---

## Success Metrics

### User Engagement
- Daily Active Users
- Questions per session
- Session duration
- Return rate (week 1, month 1)

### Learning Outcomes
- Accuracy improvement over time
- Weak area reduction
- Mock exam score progression

### Business (Future)
- Free → Paid conversion
- Subscriber retention
- NPS score

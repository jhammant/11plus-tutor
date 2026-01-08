# ExamTutor: AI-Powered UK Exam Preparation Platform

## Executive Summary

An AI-powered learning platform for UK students preparing for **11+ entrance exams** and **GCSEs**, building on the architecture of the Ilya's Top 30 project. The platform will provide personalized tutoring, practice question generation, and curriculum-aligned learning using RAG over official educational content.

---

## Market Analysis

### Target Market Size
- **UK Private Tutoring Market**: £7B annually
- **Global AI in Education**: $3.43B (2023) → projected $54.5B (2032)
- **11+ Candidates**: ~100,000+ children annually across England
- **GCSE Students**: ~700,000+ students per year cohort

### Key Competitors

| Platform | Focus | Pricing | Strengths | Gaps |
|----------|-------|---------|-----------|------|
| [Atom Learning](https://atomlearning.com) | 11+ only | £49-99/month | 90k users, 89% success rate, £25M Series A | Stops at 11+, no GCSE |
| [Seneca Learning](https://senecalearning.com) | KS2-A Level | Free + Premium | 2x faster learning claim, neuroscience-based | Less personalized |
| [Medly AI](https://www.medlyai.com) | GCSE/A-Level | 5% of tutor cost | £1.7M funding, 10k users | New, limited content |
| [Third Space Learning](https://thirdspacelearning.com) | Maths only | School subscriptions | AI tutor "Skye" | Single subject |
| [GoStudent](https://www.gostudent.org) | Human tutors | £20-40/hour | Europe's largest | Expensive, not AI-native |

### Our Differentiation
1. **Full spectrum**: 11+ through GCSE (ages 9-16)
2. **RAG-powered**: Deep understanding from curriculum documents, not just Q&A
3. **Open-source foundation**: Built on proven DeepTutor architecture
4. **Knowledge graphs**: LightRAG for interconnected topic understanding
5. **Mark scheme alignment**: Teach exam technique, not just content

---

## Exam Landscape

### 11+ Exams (Ages 10-11)

#### Providers
| Provider | Market Share | Format | Key Regions |
|----------|-------------|--------|-------------|
| **GL Assessment** | ~70% | Multiple choice, separate papers | Kent, Bucks, Birmingham, Lincolnshire |
| **CEM (Durham)** | ~25% | Integrated papers, timed sections | Berkshire, Bexley, Gloucestershire |
| **ISEB** | ~5% | Independent schools | London independent schools |
| **CSSE** | Regional | Maths & English only | Essex consortium |

#### Subjects & Question Types

**Verbal Reasoning (21 question types in GL)**
- Synonyms / Antonyms
- Analogies (word relationships)
- Code words (letter substitution, number codes)
- Hidden words
- Compound words
- Letter sequences
- Odd one out
- Reading comprehension
- Cloze passages (fill the gap)
- Shuffled sentences

**Non-Verbal Reasoning**
- Sequences and series
- Matrices (grid completion)
- Analogies (shape relationships)
- Rotations and reflections
- Transformations
- Odd one out
- Paper folding
- Nets and cubes
- Embedded shapes
- Code breakers

**Mathematics**
- National Curriculum KS2 content
- Word problems
- Fractions, decimals, percentages
- Algebra basics
- Geometry and measures
- Data handling

**English**
- Reading comprehension
- Spelling and punctuation
- Vocabulary
- Grammar
- Creative writing (some schools)

### GCSEs (Ages 14-16)

#### Exam Boards

| Board | Market Share | Known For | Headquarters |
|-------|-------------|-----------|--------------|
| **AQA** | ~40% | Largest, straightforward | Manchester |
| **Pearson Edexcel** | ~35% | International presence | London |
| **OCR** | ~15% | Cambridge-owned, analytical | Cambridge |
| **WJEC/Eduqas** | ~8% | Wales + some England | Cardiff |
| **CCEA** | ~2% | Northern Ireland | Belfast |

#### Core Subjects (Compulsory)
- English Language (8700/1EN0)
- English Literature (8702/1ET0)
- Mathematics (8300/1MA1)
- Combined Science or Triple Science

#### Popular Options
- History, Geography
- Modern Foreign Languages (French, Spanish, German)
- Computer Science
- Art & Design
- Business Studies
- Religious Studies
- Physical Education

#### Grading
- **England**: 9-1 scale (9 highest)
- **Wales/NI**: A*-G scale
- Grade 4 = "Standard pass" (old C)
- Grade 5 = "Strong pass"

---

## Content Sourcing Strategy

### Tier 1: Official Free Sources (Priority)

#### Oak National Academy API ⭐ KEY RESOURCE
- **URL**: https://open-api.thenational.academy/
- **License**: Open Government License (free for commercial use)
- **Content**: Lessons, videos, quizzes, transcripts for KS1-4
- **Integration**: REST API for curriculum data
- **Coverage**: All core subjects, aligned to National Curriculum

#### Government National Curriculum Documents
- **KS2 Framework**: [PDF](https://assets.publishing.service.gov.uk/media/5a81a9abe5274a2e8ab55319/PRIMARY_national_curriculum.pdf)
- **KS3/4 Framework**: [PDF](https://assets.publishing.service.gov.uk/media/5da7291840f0b6598f806433/Secondary_national_curriculum_corrected_PDF.pdf)
- **License**: Crown Copyright, free to use

#### Exam Board Past Papers (Direct from boards)
- **AQA**: https://www.aqa.org.uk/find-past-papers-and-mark-schemes
- **Edexcel**: https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html
- **OCR**: https://www.ocr.org.uk/qualifications/past-paper-finder/
- **WJEC**: https://www.wjec.co.uk/qualifications/past-papers/

**Note**: Exam boards allow educational use but redistribution requires care. Best approach:
- Link to official sources rather than hosting
- Use for RAG training (transformative use)
- Generate similar-style questions rather than copying

#### GL Assessment Familiarisation Papers
- Official sample papers available free
- Purchase practice packs for fuller coverage

### Tier 2: Open Educational Resources

#### BBC Bitesize
- No API, but content is publicly accessible
- 47% of UK students use it
- Cannot redistribute, but can link/reference

#### Khan Academy
- Creative Commons content
- Good for foundational maths/science concepts
- Less UK-curriculum aligned

#### Wikipedia / Simple Wikipedia
- CC-BY-SA license
- Background context for topics

### Tier 3: Generated Content

#### AI-Generated Practice Questions
Using LLMs to generate:
- Verbal reasoning questions (based on patterns)
- Non-verbal reasoning (describe transformations)
- Maths word problems
- Comprehension passages with questions
- Mark schemes

**Quality Control Requirements**:
- Human review for accuracy
- Cross-reference with curriculum objectives
- A/B testing against real exam performance

### Tier 4: Licensed/Partnership Content

#### Publisher Partnerships (Future)
- CGP Books (dominant GCSE revision publisher)
- Collins (11+ market leader)
- Letts and Pearson revision guides
- Exam board endorsed textbooks

#### School Partnerships
- Access to anonymized performance data
- Validation of question difficulty
- Real-world testing

---

## Technical Architecture

### Core Stack (Inherited from AIEducator)

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                    │
│              React 19, TailwindCSS, port 3782           │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                      │
│                Python 3.12+, port 8001                   │
└─────────────────────────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │   Agents   │  │  LightRAG  │  │  LLM API   │
    │ (Tutoring) │  │ (Knowledge)│  │ (OpenAI/   │
    │            │  │            │  │  Ollama)   │
    └────────────┘  └────────────┘  └────────────┘
```

### New Components for ExamTutor

#### 1. Question Bank System
```python
class QuestionBank:
    - subject: str  # maths, english, vr, nvr
    - exam_type: str  # 11plus_gl, 11plus_cem, gcse_aqa, etc.
    - topic: str  # e.g., "fractions", "synonyms"
    - difficulty: int  # 1-5
    - question_text: str
    - answer_options: List[str]  # for multiple choice
    - correct_answer: str
    - mark_scheme: str  # how to award marks
    - worked_solution: str
    - source: str  # generated, oak_api, past_paper
```

#### 2. Progress Tracking
```python
class StudentProgress:
    - user_id: str
    - exam_target: str  # e.g., "gcse_maths_aqa"
    - topic_mastery: Dict[str, float]  # topic -> score 0-1
    - weak_areas: List[str]
    - practice_history: List[AttemptRecord]
    - predicted_grade: str
```

#### 3. Adaptive Learning Engine
```python
class AdaptiveLearner:
    def select_next_question(student: StudentProgress) -> Question:
        # Spaced repetition + weakness targeting

    def adjust_difficulty(performance: List[AttemptRecord]) -> int:
        # Dynamic difficulty adjustment

    def generate_revision_plan(target_date: date) -> Plan:
        # Countdown to exam scheduling
```

#### 4. Mark Scheme Evaluator
```python
class MarkSchemeEvaluator:
    def evaluate_answer(
        question: Question,
        student_answer: str,
        mark_scheme: MarkScheme
    ) -> EvaluationResult:
        # Use LLM to evaluate against mark scheme
        # Return: marks awarded, feedback, model answer
```

### Data Models

#### Curriculum Structure
```
ExamBoard
├── Specification (e.g., AQA GCSE Maths 8300)
│   ├── Paper (Paper 1: Non-Calculator)
│   │   ├── Topic (Number)
│   │   │   ├── Subtopic (Fractions)
│   │   │   │   ├── LearningObjective
│   │   │   │   └── Questions[]
```

#### 11+ Structure
```
ExamProvider (GL/CEM)
├── Subject (VR/NVR/Maths/English)
│   ├── QuestionType (e.g., "Code Words")
│   │   ├── Difficulty (1-5)
│   │   └── Questions[]
```

---

## Agent Adaptations

### From AIEducator to ExamTutor

| AIEducator Agent | ExamTutor Equivalent | Adaptations |
|------------------|---------------------|-------------|
| `guide` | `explain` | Age-appropriate language, curriculum links |
| `solve` | `work_through` | Show mark scheme alignment, exam technique |
| `research` | `explore_topic` | Link to Bitesize/Oak content |
| - | `practice` | NEW: Generate and evaluate practice questions |
| - | `revise` | NEW: Spaced repetition review |
| - | `mock_exam` | NEW: Timed exam simulation |

### New Agent: Practice Agent
```python
class PracticeAgent:
    """Generate practice questions and evaluate answers"""

    def generate_question(
        subject: str,
        topic: str,
        difficulty: int,
        style: str  # "11plus_gl", "gcse_aqa"
    ) -> Question

    def evaluate_response(
        question: Question,
        response: str
    ) -> Feedback

    def explain_mistake(
        question: Question,
        wrong_answer: str,
        correct_answer: str
    ) -> Explanation
```

### New Agent: Mock Exam Agent
```python
class MockExamAgent:
    """Simulate timed exam conditions"""

    def generate_mock_paper(
        exam_type: str,
        duration_minutes: int
    ) -> MockPaper

    def run_timed_session(
        paper: MockPaper,
        student: Student
    ) -> ExamResult

    def generate_examiner_report(
        result: ExamResult
    ) -> Report
```

---

## MVP Feature Set

### Phase 1: Foundation (11+ Focus)
- [ ] Oak Academy API integration
- [ ] Question bank for VR/NVR/Maths/English
- [ ] Basic practice mode with instant feedback
- [ ] Progress tracking per topic
- [ ] GL Assessment style questions

### Phase 2: Intelligence
- [ ] Adaptive difficulty adjustment
- [ ] Weakness identification
- [ ] Personalized revision plans
- [ ] AI-generated questions
- [ ] Parent progress reports

### Phase 3: GCSE Expansion
- [ ] AQA/Edexcel spec alignment
- [ ] Past paper integration
- [ ] Mark scheme evaluation
- [ ] Subject-specific agents
- [ ] Mock exam mode

### Phase 4: Scale
- [ ] Mobile app (React Native)
- [ ] School/tutor dashboards
- [ ] Performance analytics
- [ ] Content partnerships
- [ ] Gamification

---

## Content Pipeline

### Automated Ingestion

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   Oak API        │────▶│   ETL Pipeline   │────▶│   LightRAG       │
│   (Lessons)      │     │   (Transform)    │     │   (Index)        │
└──────────────────┘     └──────────────────┘     └──────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   Past Papers    │────▶│   Question       │────▶│   Question       │
│   (PDFs)         │     │   Extraction     │     │   Bank           │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

### Question Generation Pipeline

```python
# 1. Extract patterns from real questions
real_questions = load_past_paper("gl_vr_2023.pdf")
patterns = extract_patterns(real_questions)

# 2. Generate similar questions
generated = llm.generate(
    prompt=f"""Generate a {pattern.type} question
    similar in style to: {pattern.example}
    Topic: {pattern.topic}
    Difficulty: {pattern.difficulty}"""
)

# 3. Validate
validated = human_review(generated)

# 4. Store
question_bank.add(validated)
```

---

## Legal Considerations

### Safe to Use
- Oak National Academy content (Open Government License)
- National Curriculum documents (Crown Copyright)
- Past papers for personal study/RAG training
- AI-generated original questions

### Requires Care
- Past papers for redistribution (link, don't host)
- Publisher content (licensing required)
- BBC Bitesize content (reference, don't copy)

### Must Avoid
- Copying current year exam papers
- Redistributing purchased practice papers
- Using content without attribution where required

### Recommended Approach
1. **Primary**: Oak API + AI generation
2. **Secondary**: Links to official exam board papers
3. **Future**: Publisher licensing deals

---

## Monetization Options

### B2C (Direct to families)
- Freemium: Basic practice free, advanced features paid
- Subscription: £9.99-29.99/month (undercut Atom's £49-99)
- Pay-per-mock: £2.99 per full mock exam

### B2B (Schools/Tutors)
- School licenses: £500-2000/year
- Tutor tools: £29.99/month
- White-label options

### Marketplace
- Tutor-created content (revenue share)
- Premium question packs

---

## Success Metrics

### Learning Outcomes
- Topic mastery improvement
- Mock exam score progression
- Correlation with real exam results

### Engagement
- Daily active users
- Questions attempted per session
- Session duration
- Retention (week 1, month 1, month 3)

### Business
- Free → Paid conversion rate
- Customer acquisition cost
- Lifetime value
- NPS score

---

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Content accuracy errors | High | Medium | Human review, user reporting, rapid fixes |
| Copyright claims | High | Low | Stick to OGL content, clear attribution |
| Competitor response | Medium | High | Speed to market, differentiation |
| AI hallucination in answers | High | Medium | Structured outputs, validation layers |
| Exam format changes | Medium | Medium | Modular content system, quick updates |

---

## Implementation Roadmap

### Month 1: Foundation
- Fork AIEducator architecture
- Oak Academy API integration
- Basic question bank schema
- 11+ VR question types (5 types)

### Month 2: Core Features
- All 21 VR question types
- NVR question types
- Practice mode with feedback
- Basic progress tracking

### Month 3: Intelligence
- Adaptive difficulty
- Weakness detection
- AI question generation
- Parent dashboard

### Month 4: GCSE Start
- GCSE Maths (AQA) spec mapping
- Past paper integration
- Mark scheme evaluation
- Mock exam mode

### Month 5-6: Polish & Launch
- Mobile responsiveness
- Performance optimization
- Beta testing with families
- Launch marketing

---

## Next Steps

1. **Validate Oak API** - Test integration, assess content coverage
2. **Design question schema** - Finalize data models
3. **Build 11+ VR prototype** - 5 question types, basic practice
4. **User testing** - Find 10 families for feedback
5. **Iterate** - Based on feedback, expand coverage

---

## Appendix: Research Sources

### Official Resources
- [Oak National Academy API](https://open-api.thenational.academy/)
- [GOV.UK National Curriculum](https://www.gov.uk/government/collections/national-curriculum)
- [AQA Past Papers](https://www.aqa.org.uk/find-past-papers-and-mark-schemes)
- [Edexcel Past Papers](https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html)
- [OCR Past Papers](https://www.ocr.org.uk/qualifications/past-paper-finder/)
- [GL Assessment Official](https://11plus.gl-assessment.co.uk/)

### Free Practice Resources
- [SATs Papers UK](https://www.sats-papers.co.uk/11-plus-papers/) - 450+ free 11+ papers
- [CGP Free Practice](https://www.cgpbooks.co.uk/info/preparing-for-the-11-plus-with-cgp/free-11-plus-practice-tests)
- [Maths Genie](https://www.mathsgenie.co.uk/) - Free GCSE maths

### Competitor Research
- [Atom Learning](https://atomlearning.com)
- [Seneca Learning](https://senecalearning.com)
- [Medly AI](https://www.medlyai.com)
- [Third Space Learning](https://thirdspacelearning.com)

### Technical References
- [Bond 11+ Guide: GL vs CEM](https://www.bond11plus.co.uk/11-plus-cem-gl)
- [Verbal Reasoning Question Types](https://www.achievelearning.co.uk/verbal-reasoning-question-types-your-complete-guide/)
- [Non-Verbal Reasoning Guide](https://www.u2tuition.com/resources/11-plus-non-verbal-reasoning)
- [GCSE Exam Boards Explained](https://www.atomlearning.com/blog/exam-boards-explained)

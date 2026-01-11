"""
11+ Tutor API
FastAPI backend for the 11+ exam preparation platform
"""

import os
import sys
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import uuid

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.database import get_db, init_db, Question as DBQuestion, Attempt as DBAttempt
from src.core.database import Student as DBStudent, TopicProgress as DBTopicProgress
from sqlalchemy.orm import Session
from settings import settings

# ============================================================================
# Pydantic Models
# ============================================================================

class QuestionResponse(BaseModel):
    id: str
    exam_type: str
    subject: str
    topic: Optional[str]
    question_type: str
    difficulty: int
    question_text: str
    options: Optional[List[str]]
    marks_available: int
    hint: Optional[str] = None

    class Config:
        from_attributes = True


class QuestionWithAnswer(QuestionResponse):
    correct_answer: str
    correct_index: Optional[int]
    worked_solution: Optional[str]
    explanation: Optional[str] = None


class AnswerSubmission(BaseModel):
    question_id: str
    student_id: str
    answer: str
    time_taken_seconds: int = 0


class AnswerResult(BaseModel):
    is_correct: bool
    marks_awarded: int
    marks_available: int
    correct_answer: str
    feedback: str
    worked_solution: Optional[str]


class GenerateRequest(BaseModel):
    subject: str
    question_type: str
    difficulty: int = 3
    count: int = 1


class StudentProgress(BaseModel):
    student_id: str
    subject: str
    total_attempted: int
    total_correct: int
    accuracy: float
    topics: dict


# ============================================================================
# FastAPI App
# ============================================================================

app = FastAPI(
    title="11+ Tutor API",
    description="Free, open-source AI-powered 11+ exam preparation",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3783", "http://127.0.0.1:3783"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Startup
# ============================================================================

@app.on_event("startup")
async def startup():
    """Initialize database on startup"""
    init_db()


# ============================================================================
# Health Check
# ============================================================================

@app.get("/")
async def root():
    return {
        "name": "11+ Tutor API",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


# ============================================================================
# Questions Endpoints
# ============================================================================

@app.get("/api/questions", response_model=List[QuestionResponse])
async def get_questions(
    subject: Optional[str] = None,
    question_type: Optional[str] = None,
    difficulty: Optional[int] = None,
    exam_type: str = "11plus_gl",
    limit: int = Query(default=10, le=100),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get questions from the question bank"""
    query = db.query(DBQuestion).filter(DBQuestion.exam_type == exam_type)

    if subject:
        query = query.filter(DBQuestion.subject == subject)
    if question_type:
        query = query.filter(DBQuestion.question_type == question_type)
    if difficulty:
        query = query.filter(DBQuestion.difficulty == difficulty)

    questions = query.offset(offset).limit(limit).all()
    return questions


@app.get("/api/questions/count")
async def get_question_count(
    subject: Optional[str] = None,
    question_type: Optional[str] = None,
    exam_type: str = "11plus_gl",
    db: Session = Depends(get_db)
):
    """Get total count of questions"""
    query = db.query(DBQuestion).filter(DBQuestion.exam_type == exam_type)

    if subject:
        query = query.filter(DBQuestion.subject == subject)
    if question_type:
        query = query.filter(DBQuestion.question_type == question_type)

    count = query.count()
    return {"count": count}


@app.get("/api/questions/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: str, db: Session = Depends(get_db)):
    """Get a specific question (without answer)"""
    question = db.query(DBQuestion).filter(DBQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@app.get("/api/questions/{question_id}/answer", response_model=QuestionWithAnswer)
async def get_question_with_answer(question_id: str, db: Session = Depends(get_db)):
    """Get a question with its answer and solution"""
    question = db.query(DBQuestion).filter(DBQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@app.get("/api/questions/random", response_model=QuestionResponse)
async def get_random_question(
    subject: Optional[str] = None,
    question_type: Optional[str] = None,
    difficulty: Optional[int] = None,
    exam_type: str = "11plus_gl",
    db: Session = Depends(get_db)
):
    """Get a random question matching criteria"""
    from sqlalchemy.sql.expression import func

    query = db.query(DBQuestion).filter(DBQuestion.exam_type == exam_type)

    if subject:
        query = query.filter(DBQuestion.subject == subject)
    if question_type:
        query = query.filter(DBQuestion.question_type == question_type)
    if difficulty:
        query = query.filter(DBQuestion.difficulty == difficulty)

    question = query.order_by(func.random()).first()
    if not question:
        raise HTTPException(status_code=404, detail="No questions found matching criteria")
    return question


# ============================================================================
# Answer Submission
# ============================================================================

@app.post("/api/submit", response_model=AnswerResult)
async def submit_answer(submission: AnswerSubmission, db: Session = Depends(get_db)):
    """Submit an answer and get feedback"""

    # Get the question
    question = db.query(DBQuestion).filter(DBQuestion.id == submission.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Check answer - multiple methods for different question types
    submitted_answer = submission.answer.strip()
    correct_answer = question.correct_answer.strip()
    is_correct = False

    # Method 1: Direct string comparison (case-insensitive)
    if submitted_answer.lower() == correct_answer.lower():
        is_correct = True

    # Method 2: Check by index if options exist and correct_index is set
    if not is_correct and question.options and question.correct_index is not None:
        options = question.options if isinstance(question.options, list) else json.loads(question.options)

        # If submitted answer matches option at correct_index
        if question.correct_index < len(options):
            correct_option = options[question.correct_index]
            if submitted_answer == correct_option:
                is_correct = True
            # Also check case-insensitive for text options
            elif submitted_answer.lower() == str(correct_option).lower():
                is_correct = True

        # If submitted answer is an index number
        if submitted_answer.isdigit():
            answer_index = int(submitted_answer)
            if answer_index == question.correct_index:
                is_correct = True

    marks = question.marks_available if is_correct else 0

    # Record the attempt
    attempt = DBAttempt(
        id=str(uuid.uuid4()),
        student_id=submission.student_id,
        question_id=question.id,
        student_answer=submission.answer,
        time_taken_seconds=submission.time_taken_seconds,
        is_correct=is_correct,
        marks_awarded=marks,
        marks_available=question.marks_available,
    )
    db.add(attempt)

    # Update question statistics (handle None values from newly generated questions)
    question.times_attempted = (question.times_attempted or 0) + 1
    if is_correct:
        question.times_correct = (question.times_correct or 0) + 1

    db.commit()

    # Generate feedback
    if is_correct:
        feedback = "Correct! Well done."
    else:
        feedback = f"Not quite. The correct answer was: {question.correct_answer}"

    return AnswerResult(
        is_correct=is_correct,
        marks_awarded=marks,
        marks_available=question.marks_available,
        correct_answer=question.correct_answer,
        feedback=feedback,
        worked_solution=question.worked_solution,
    )


# ============================================================================
# Progress Tracking
# ============================================================================

@app.get("/api/progress/{student_id}")
async def get_progress(student_id: str, db: Session = Depends(get_db)):
    """Get student's overall progress"""

    attempts = db.query(DBAttempt).filter(DBAttempt.student_id == student_id).all()

    if not attempts:
        return {
            "student_id": student_id,
            "total_attempted": 0,
            "total_correct": 0,
            "accuracy": 0,
            "subjects": {},
            "recent_activity": []
        }

    total = len(attempts)
    correct = sum(1 for a in attempts if a.is_correct)

    # Group by subject
    subjects = {}
    for attempt in attempts:
        question = db.query(DBQuestion).filter(DBQuestion.id == attempt.question_id).first()
        if question:
            if question.subject not in subjects:
                subjects[question.subject] = {"attempted": 0, "correct": 0}
            subjects[question.subject]["attempted"] += 1
            if attempt.is_correct:
                subjects[question.subject]["correct"] += 1

    return {
        "student_id": student_id,
        "total_attempted": total,
        "total_correct": correct,
        "accuracy": round(correct / total * 100, 1) if total > 0 else 0,
        "subjects": subjects,
    }


# ============================================================================
# Question Types Info
# ============================================================================

@app.get("/api/question-types")
async def get_question_types():
    """Get available question types"""
    return {
        "verbal_reasoning": [
            "synonyms", "antonyms", "analogies", "odd_one_out",
            "code_words", "letter_sequences", "hidden_words", "compound_words"
        ],
        "non_verbal_reasoning": [
            "sequences", "matrices", "analogies", "odd_one_out",
            "rotations", "reflections", "transformations"
        ],
        "mathematics": [
            "arithmetic", "fractions", "percentages", "ratio",
            "algebra", "geometry", "word_problems", "sequences"
        ],
        "english": [
            "comprehension", "spelling", "punctuation", "grammar", "vocabulary"
        ]
    }


@app.get("/api/exam-types")
async def get_exam_types():
    """Get supported exam types (11+ only for this version)"""
    return {
        "11plus": {
            "11plus_gl": "GL Assessment (most common)",
            "11plus_cem": "CEM (Durham University)",
        }
    }


# ============================================================================
# Features Endpoint (for opensource vs paid)
# ============================================================================

@app.get("/api/features")
async def get_features():
    """Get enabled features based on app mode (opensource vs paid)"""
    return {
        "app_mode": settings.app_mode,
        "features": settings.get_enabled_features(),
        "limits": {
            "daily_ai_questions": settings.daily_ai_questions_limit,
            "daily_ai_tutor_messages": settings.daily_ai_tutor_messages,
        }
    }


@app.get("/api/config")
async def get_config():
    """Get basic app configuration"""
    return {
        "app_name": "11+ Tutor",
        "version": "1.0.0",
        "mode": settings.app_mode,
        "is_paid": settings.is_paid_mode(),
    }


# ============================================================================
# Strategy Guides Endpoints
# ============================================================================

import yaml
from pathlib import Path as FilePath

STRATEGIES_DIR = FilePath(__file__).parent.parent.parent / "data" / "strategies"
LESSONS_DIR = FilePath(__file__).parent.parent.parent / "data" / "lessons"


@app.get("/api/strategies")
async def get_strategies():
    """Get list of all strategy guides"""
    strategies = []

    if STRATEGIES_DIR.exists():
        for file in STRATEGIES_DIR.glob("*.yaml"):
            try:
                with open(file, "r") as f:
                    data = yaml.safe_load(f)
                    strategies.append({
                        "question_type": data.get("question_type"),
                        "subject": data.get("subject"),
                        "title": data.get("title"),
                        "is_free": data.get("is_free", True),
                        "difficulty_range": data.get("difficulty_range"),
                    })
            except Exception as e:
                print(f"Error loading strategy {file}: {e}")

    return {"strategies": strategies}


@app.get("/api/strategies/{question_type}")
async def get_strategy(question_type: str):
    """Get a specific strategy guide"""
    file_path = STRATEGIES_DIR / f"{question_type}.yaml"

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Strategy guide for '{question_type}' not found")

    try:
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
            return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading strategy: {str(e)}")


# ============================================================================
# Learning Content Endpoints
# ============================================================================

@app.get("/api/learn/subjects")
async def get_learn_subjects():
    """Get subjects available for learning with topic counts"""
    # Define the learning structure
    subjects = [
        {
            "id": "verbal_reasoning",
            "name": "Verbal Reasoning",
            "description": "Words, meanings, and logic",
            "icon": "PenTool",
            "color": "purple",
            "topics": [
                {"id": "synonyms", "name": "Synonyms", "lesson_count": 1},
                {"id": "antonyms", "name": "Antonyms", "lesson_count": 1},
                {"id": "analogies", "name": "Analogies", "lesson_count": 1},
                {"id": "odd_one_out", "name": "Odd One Out", "lesson_count": 1},
                {"id": "code_words", "name": "Code Words", "lesson_count": 1},
                {"id": "letter_sequences", "name": "Letter Sequences", "lesson_count": 1},
            ]
        },
        {
            "id": "mathematics",
            "name": "Mathematics",
            "description": "Numbers, shapes, and problem solving",
            "icon": "Calculator",
            "color": "green",
            "topics": [
                {"id": "arithmetic", "name": "Arithmetic", "lesson_count": 1},
                {"id": "fractions", "name": "Fractions", "lesson_count": 1},
                {"id": "sequences", "name": "Number Sequences", "lesson_count": 1},
                {"id": "percentages", "name": "Percentages", "lesson_count": 0},
                {"id": "word_problems", "name": "Word Problems", "lesson_count": 0},
            ]
        },
        {
            "id": "non_verbal_reasoning",
            "name": "Non-Verbal Reasoning",
            "description": "Patterns, shapes, and spatial thinking",
            "icon": "Puzzle",
            "color": "blue",
            "topics": [
                {"id": "pattern_sequences", "name": "Pattern Sequences", "lesson_count": 0},
                {"id": "matrices", "name": "Matrices", "lesson_count": 0},
                {"id": "rotations", "name": "Rotations & Reflections", "lesson_count": 0},
            ]
        },
        {
            "id": "english",
            "name": "English",
            "description": "Reading, writing, and comprehension",
            "icon": "BookOpen",
            "color": "amber",
            "topics": [
                {"id": "comprehension", "name": "Comprehension", "lesson_count": 0},
                {"id": "vocabulary", "name": "Vocabulary", "lesson_count": 0},
                {"id": "grammar", "name": "Grammar", "lesson_count": 0},
            ]
        }
    ]

    return {"subjects": subjects}


@app.get("/api/learn/{subject}/{topic}")
async def get_lesson(subject: str, topic: str):
    """Get lesson content for a specific topic"""
    # First check if there's a YAML file for this lesson
    lesson_file = LESSONS_DIR / subject / f"{topic}.yaml"

    if lesson_file.exists():
        try:
            with open(lesson_file, "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading lesson: {str(e)}")

    # If no lesson file, check if there's a corresponding strategy guide
    strategy_file = STRATEGIES_DIR / f"{topic}.yaml"
    if strategy_file.exists():
        try:
            with open(strategy_file, "r") as f:
                data = yaml.safe_load(f)
                # Convert strategy to lesson format
                return {
                    "subject": subject,
                    "topic": topic,
                    "title": data.get("title", topic.replace("_", " ").title()),
                    "explanation": data.get("what_is_it", ""),
                    "key_points": data.get("approach", []),
                    "worked_examples": data.get("worked_examples", []),
                    "tips": data.get("time_tips", []),
                    "common_mistakes": data.get("common_mistakes", []),
                    "is_free": data.get("is_free", True),
                }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading content: {str(e)}")

    raise HTTPException(status_code=404, detail=f"Lesson for '{subject}/{topic}' not found")


# ============================================================================
# Run
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

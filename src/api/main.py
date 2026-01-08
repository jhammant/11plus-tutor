"""
ExamTutor API
FastAPI backend for the exam preparation platform
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
    title="ExamTutor API",
    description="AI-powered UK exam preparation platform",
    version="0.1.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3782", "http://127.0.0.1:3782"],
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
        "name": "ExamTutor API",
        "version": "0.1.0",
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

    # Check answer
    is_correct = submission.answer.strip().lower() == question.correct_answer.strip().lower()

    # For multiple choice, also check by index
    if question.options and submission.answer.isdigit():
        answer_index = int(submission.answer)
        if 0 <= answer_index < len(question.options):
            is_correct = answer_index == question.correct_index

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

    # Update question statistics
    question.times_attempted += 1
    if is_correct:
        question.times_correct += 1

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
    """Get supported exam types"""
    return {
        "11plus": {
            "11plus_gl": "GL Assessment (most common)",
            "11plus_cem": "CEM (Durham University)",
        },
        "gcse": {
            "gcse_aqa": "AQA",
            "gcse_edexcel": "Pearson Edexcel",
            "gcse_ocr": "OCR",
        }
    }


# ============================================================================
# Run
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

"""
Database Setup and Models
SQLite database for questions, progress, and user data
"""

import os
from datetime import datetime
from typing import Optional, List
from pathlib import Path

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Database path
DB_PATH = Path(__file__).parent.parent.parent / "examtutor.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

# Create engine
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ============================================================================
# Database Models
# ============================================================================

class Question(Base):
    """Question bank table"""
    __tablename__ = "questions"

    id = Column(String, primary_key=True)
    exam_type = Column(String, nullable=False, index=True)  # 11plus_gl, gcse_aqa, etc.
    subject = Column(String, nullable=False, index=True)  # verbal_reasoning, maths, etc.
    topic = Column(String, index=True)
    subtopic = Column(String)
    question_type = Column(String, nullable=False, index=True)  # synonyms, antonyms, etc.
    difficulty = Column(Integer, default=3)  # 1-5

    # Content
    question_text = Column(Text, nullable=False)
    question_image = Column(String)  # Path or URL
    context = Column(Text)  # Additional context like passages

    # Answer
    options = Column(JSON)  # List of options for multiple choice
    correct_answer = Column(String, nullable=False)
    correct_index = Column(Integer)
    marks_available = Column(Integer, default=1)
    mark_scheme = Column(Text)
    worked_solution = Column(Text)
    hint = Column(Text)

    # Metadata
    source = Column(String, default="generated")  # generated, oak_api, past_paper
    source_reference = Column(String)
    tags = Column(JSON)  # List of tags
    created_at = Column(DateTime, default=datetime.utcnow)

    # Statistics
    times_attempted = Column(Integer, default=0)
    times_correct = Column(Integer, default=0)

    # Relationships
    attempts = relationship("Attempt", back_populates="question")


class Student(Base):
    """Student profiles"""
    __tablename__ = "students"

    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    age = Column(Integer)
    year_group = Column(Integer)  # School year

    # Target exam
    exam_target = Column(String)  # e.g., "11plus_gl", "gcse_aqa_maths"
    target_date = Column(DateTime)

    # Settings
    preferred_difficulty = Column(Integer, default=3)
    daily_goal_questions = Column(Integer, default=20)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)

    # Relationships
    attempts = relationship("Attempt", back_populates="student")
    progress = relationship("TopicProgress", back_populates="student")


class Attempt(Base):
    """Record of question attempts"""
    __tablename__ = "attempts"

    id = Column(String, primary_key=True)
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    question_id = Column(String, ForeignKey("questions.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Response
    student_answer = Column(String)
    time_taken_seconds = Column(Integer)

    # Evaluation
    is_correct = Column(Boolean)
    marks_awarded = Column(Integer, default=0)
    marks_available = Column(Integer, default=1)

    # Feedback
    feedback = Column(Text)
    hint_used = Column(Boolean, default=False)
    solution_viewed = Column(Boolean, default=False)

    # Relationships
    student = relationship("Student", back_populates="attempts")
    question = relationship("Question", back_populates="attempts")


class TopicProgress(Base):
    """Track mastery per topic"""
    __tablename__ = "topic_progress"

    id = Column(String, primary_key=True)
    student_id = Column(String, ForeignKey("students.id"), nullable=False)

    # Topic
    subject = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    question_type = Column(String)

    # Mastery
    mastery_score = Column(Float, default=0.0)  # 0.0 to 1.0
    total_attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)

    # Spaced repetition
    last_practiced = Column(DateTime)
    next_review = Column(DateTime)
    ease_factor = Column(Float, default=2.5)  # SM-2 algorithm
    interval_days = Column(Integer, default=1)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="progress")


class MockExam(Base):
    """Mock exam papers"""
    __tablename__ = "mock_exams"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    exam_type = Column(String, nullable=False)
    subject = Column(String, nullable=False)

    # Configuration
    time_limit_minutes = Column(Integer, default=45)
    question_ids = Column(JSON)  # List of question IDs
    total_marks = Column(Integer)
    instructions = Column(Text)
    calculator_allowed = Column(Boolean, default=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)


class MockExamResult(Base):
    """Results of completed mock exams"""
    __tablename__ = "mock_exam_results"

    id = Column(String, primary_key=True)
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    mock_exam_id = Column(String, ForeignKey("mock_exams.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Performance
    time_taken_minutes = Column(Integer)
    marks_achieved = Column(Integer)
    marks_available = Column(Integer)
    percentage = Column(Float)
    grade = Column(String)

    # Analysis
    question_results = Column(JSON)  # List of attempt records
    strong_topics = Column(JSON)
    weak_topics = Column(JSON)
    examiner_feedback = Column(Text)


class LearningStreak(Base):
    """Track daily learning streaks"""
    __tablename__ = "learning_streaks"

    id = Column(String, primary_key=True)
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    questions_completed = Column(Integer, default=0)
    time_spent_minutes = Column(Integer, default=0)
    topics_practiced = Column(JSON)


# ============================================================================
# Database Functions
# ============================================================================

def init_db():
    """Initialize the database tables"""
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized at: {DB_PATH}")


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed_sample_data():
    """Seed the database with sample data for testing"""
    import uuid

    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(Question).count() > 0:
            print("Database already has data, skipping seed")
            return

        # Sample questions
        sample_questions = [
            {
                "id": str(uuid.uuid4()),
                "exam_type": "11plus_gl",
                "subject": "verbal_reasoning",
                "topic": "vocabulary",
                "question_type": "synonyms",
                "difficulty": 2,
                "question_text": "Find two words, one from each group, that are closest in meaning.\n(happy, sad, angry) (joyful, upset, calm)",
                "options": ["happy & joyful", "happy & upset", "sad & joyful", "angry & calm", "sad & upset"],
                "correct_answer": "happy & joyful",
                "correct_index": 0,
                "marks_available": 1,
                "worked_solution": "Happy and joyful are synonyms - they both mean feeling pleasure or contentment.",
                "source": "sample",
            },
            {
                "id": str(uuid.uuid4()),
                "exam_type": "11plus_gl",
                "subject": "verbal_reasoning",
                "topic": "vocabulary",
                "question_type": "antonyms",
                "difficulty": 2,
                "question_text": "Find two words, one from each group, that are most opposite in meaning.\n(hot, warm, tepid) (cold, cool, lukewarm)",
                "options": ["hot & cold", "hot & lukewarm", "warm & cool", "tepid & cold", "warm & lukewarm"],
                "correct_answer": "hot & cold",
                "correct_index": 0,
                "marks_available": 1,
                "worked_solution": "Hot and cold are antonyms - they represent opposite ends of the temperature scale.",
                "source": "sample",
            },
            {
                "id": str(uuid.uuid4()),
                "exam_type": "11plus_gl",
                "subject": "mathematics",
                "topic": "arithmetic",
                "question_type": "word_problem",
                "difficulty": 3,
                "question_text": "Sarah has 24 sweets. She gives 1/3 of them to Tom and 1/4 of them to Emma. How many sweets does Sarah have left?",
                "options": ["8", "10", "12", "14", "16"],
                "correct_answer": "10",
                "correct_index": 1,
                "marks_available": 2,
                "worked_solution": "1/3 of 24 = 8 sweets to Tom\n1/4 of 24 = 6 sweets to Emma\nTotal given away = 8 + 6 = 14\nSweets left = 24 - 14 = 10",
                "source": "sample",
            },
        ]

        for q_data in sample_questions:
            question = Question(**q_data)
            db.add(question)

        db.commit()
        print(f"Seeded {len(sample_questions)} sample questions")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing ExamTutor database...")
    init_db()
    seed_sample_data()
    print("Done!")

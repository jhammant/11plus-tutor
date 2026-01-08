#!/usr/bin/env python3
"""
Import generated questions into the database
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.database import SessionLocal, Question, init_db


def import_questions():
    """Import questions from JSON into database"""
    questions_file = Path(__file__).parent.parent / "data" / "questions" / "all_questions.json"

    if not questions_file.exists():
        print(f"No questions file found at {questions_file}")
        return

    with open(questions_file) as f:
        questions = json.load(f)

    print(f"Found {len(questions)} questions to import")

    init_db()
    db = SessionLocal()

    imported = 0
    skipped = 0

    for q in questions:
        # Check if already exists
        existing = db.query(Question).filter(Question.id == q['id']).first()
        if existing:
            skipped += 1
            continue

        # Create question record
        question = Question(
            id=q['id'],
            exam_type=q['exam_type'],
            subject=q['subject'],
            topic=q.get('topic', 'general'),
            question_type=q['question_type'],
            difficulty=q['difficulty'],
            question_text=q['question_text'],
            options=q['options'],
            correct_answer=q['correct_answer'],
            correct_index=q['correct_index'],
            marks_available=1,
            worked_solution=q.get('explanation'),
            source='generated',
        )

        db.add(question)
        imported += 1

    db.commit()
    db.close()

    total = db.query(Question).count() if False else imported + skipped
    print(f"Imported: {imported}")
    print(f"Skipped (already exist): {skipped}")

    # Get final count
    db = SessionLocal()
    total = db.query(Question).count()
    db.close()
    print(f"Total questions in database: {total}")


if __name__ == "__main__":
    import_questions()

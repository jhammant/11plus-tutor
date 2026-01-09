#!/usr/bin/env python3
"""
Import generated questions from JSON files into the SQLite database.
"""

import os
import sys
import json
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.database import get_db, init_db, Question
from sqlalchemy.orm import Session

DATA_DIR = Path(__file__).parent.parent / "data" / "questions"


def import_from_file(filepath: Path, db: Session) -> int:
    """Import questions from a single JSON file."""
    imported = 0
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Handle both single question and list of questions
        questions = data if isinstance(data, list) else [data]

        for q in questions:
            # Check if question already exists
            existing = db.query(Question).filter(Question.id == q.get("id")).first()
            if existing:
                continue

            question = Question(
                id=q.get("id"),
                exam_type=q.get("exam_type", "11plus_gl"),
                subject=q.get("subject", "unknown"),
                topic=q.get("topic", "general"),
                question_type=q.get("question_type", "unknown"),
                difficulty=q.get("difficulty", 3),
                question_text=q.get("question_text", q.get("question", "")),
                options=q.get("options", []),
                correct_answer=q.get("correct_answer", ""),
                correct_index=q.get("correct_index"),
                worked_solution=q.get("worked_solution", q.get("explanation", "")),
                marks_available=q.get("marks_available", 1),
                hint=q.get("hint"),
            )
            db.add(question)
            imported += 1

        db.commit()
    except json.JSONDecodeError as e:
        print(f"  Error parsing {filepath}: {e}")
    except Exception as e:
        print(f"  Error importing {filepath}: {e}")
        db.rollback()

    return imported


def import_all_questions():
    """Import all questions from JSON files."""
    print("ExamTutor Question Importer")
    print("=" * 40)

    # Initialize database
    init_db()

    # Get database session
    db = next(get_db())

    total_imported = 0

    # Check for all_questions.json first
    all_questions_file = DATA_DIR / "all_questions.json"
    if all_questions_file.exists():
        print(f"\nImporting from all_questions.json...")
        count = import_from_file(all_questions_file, db)
        print(f"  Imported {count} questions")
        total_imported += count

    # Also scan individual question files
    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith('.json') and file != 'all_questions.json':
                filepath = Path(root) / file
                count = import_from_file(filepath, db)
                if count > 0:
                    print(f"  Imported {count} from {filepath.name}")
                    total_imported += count

    # Count total in database
    total_in_db = db.query(Question).count()

    print(f"\n{'=' * 40}")
    print(f"Import complete!")
    print(f"  New questions imported: {total_imported}")
    print(f"  Total questions in database: {total_in_db}")

    # Show breakdown by subject
    print(f"\nBy Subject:")
    for subject in ["verbal_reasoning", "mathematics", "non_verbal_reasoning", "english"]:
        count = db.query(Question).filter(Question.subject == subject).count()
        if count > 0:
            print(f"  {subject}: {count}")

    print(f"\nBy Type:")
    types = db.query(Question.question_type).distinct().all()
    for (qtype,) in types:
        count = db.query(Question).filter(Question.question_type == qtype).count()
        print(f"  {qtype}: {count}")

    db.close()


if __name__ == "__main__":
    import_all_questions()

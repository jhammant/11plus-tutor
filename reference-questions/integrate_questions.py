"""
Question Bank Integration Script
Integrates OCR-extracted questions into the main question bank and manages adaptive difficulty.
"""

import json
from pathlib import Path
from datetime import datetime

# Import models from question_bank
from src.question_bank.models import (
    Question,
    ExamType,
    Subject,
    Difficulty,
    QuestionFormat,
    QuestionBank,
    AdaptiveDifficultyConfig
)


def load_extracted_questions(json_path: str) -> list:
    """Load extracted questions from JSON file"""
    with open(json_path, 'r') as f:
        return json.load(f)


def validate_question(question_data: dict) -> bool:
    """Validate a question's structure and content"""
    required_fields = ['id', 'question_text', 'correct_answer']
    return all(field in question_data for field in required_fields)


def normalize_difficulty(difficulty_str: str) -> Difficulty:
    """Map difficulty string to enum"""
    mapping = {
        'foundation': Difficulty.FOUNDATION,
        'easy': Difficulty.EASY,
        'medium': Difficulty.MEDIUM,
        'hard': Difficulty.HARD,
        'challenge': Difficulty.CHALLENGE
    }
    return mapping.get(difficulty_str.lower(), Difficulty.MEDIUM)


def normalize_subject(subject_str: str) -> Subject:
    """Map subject string to enum"""
    mapping = {
        'verbal_reasoning': Subject.VERBAL_REASONING,
        'non_verbal_reasoning': Subject.NON_VERBAL_REASONING,
        'mathematics': Subject.MATHEMATICS,
        'english': Subject.ENGLISH
    }
    return mapping.get(subject_str.lower(), Subject.MATHEMATICS)


def normalize_format(format_str: str) -> QuestionFormat:
    """Map format string to enum"""
    mapping = {
        'multiple_choice': QuestionFormat.MULTIPLE_CHOICE,
        'short_answer': QuestionFormat.SHORT_ANSWER,
        'long_answer': QuestionFormat.LONG_ANSWER,
        'fill_blank': QuestionFormat.FILL_BLANK
    }
    return mapping.get(format_str.lower(), QuestionFormat.MULTIPLE_CHOICE)


def normalize_exam_type(exam_str: str) -> ExamType:
    """Map exam type string to enum"""
    mapping = {
        '11plus_gl': ExamType.ELEVEN_PLUS_GL,
        '11plus_cem': ExamType.ELEVEN_PLUS_CEM,
        'gcse_aqa': ExamType.GCSE_AQA,
        'gcse_edexcel': ExamType.GCSE_EDEXCEL,
        'gcse_ocr': ExamType.GCSE_OCR
    }
    return mapping.get(exam_str.lower(), ExamType.ELEVEN_PLUS_GL)


def process_extracted_questions(extracted_questions: list) -> list:
    """Process and normalize extracted questions"""
    processed = []
    
    for q in extracted_questions:
        if not validate_question(q):
            print(f"Skipping invalid question: {q.get('id', 'unknown')}")
            continue
        
        processed_question = Question(
            id=q['id'],
            exam_type=normalize_exam_type(q.get('exam_type', '11plus_gl')),
            subject=normalize_subject(q.get('subject', 'mathematics')),
            topic=q.get('topic', 'General'),
            subtopic=q.get('subtopic'),
            question_type=q.get('question_type', 'general'),
            difficulty=normalize_difficulty(q.get('difficulty', 'medium')),
            format=normalize_format(q.get('format', 'multiple_choice')),
            question_text=q['question_text'],
            correct_answer=q['correct_answer'],
            options=q.get('options'),
            question_image=q.get('question_image'),
            context=q.get('context'),
            worked_solution=q.get('worked_solution'),
            hint=q.get('hint'),
            source='ocr_extracted',
            tags=q.get('tags', [])
        )
        
        processed.append(processed_question)
    
    return processed


def merge_questions(main_bank: QuestionBank, new_questions: list) -> QuestionBank:
    """Merge new questions into the main question bank"""
    # Create a set of existing question IDs
    existing_ids = {q.id for q in main_bank.questions}
    
    # Add only new questions
    for question in new_questions:
        if question.id not in existing_ids:
            main_bank.questions.append(question)
    
    return main_bank


def update_question_statistics(main_bank: QuestionBank, attempts: list) -> QuestionBank:
    """Update question statistics based on student attempts"""
    for attempt in attempts:
        question = main_bank.get_question_by_id(attempt.question_id)
        if question:
            question.times_attempted += 1
            if attempt.is_correct:
                question.times_correct += 1
    
    return main_bank


def get_adaptive_difficulty(student_progress, question_bank: QuestionBank) -> Difficulty:
    """Calculate adaptive difficulty based on student performance"""
    config = question_bank.difficulty_config
    
    # Calculate accuracy
    if student_progress.total_questions_attempted == 0:
        return config.initial_difficulty
    
    accuracy = student_progress.total_correct / student_progress.total_questions_attempted
    
    # Adjust difficulty based on accuracy
    if accuracy >= 0.85:
        return config.max_difficulty
    elif accuracy >= 0.7:
        return Difficulty.HARD
    elif accuracy >= 0.55:
        return Difficulty.MEDIUM
    elif accuracy >= 0.4:
        return Difficulty.EASY
    else:
        return config.min_difficulty


def main():
    # Load extracted questions
    extracted_questions_path = "reference-questions/extracted_questions.json"
    extracted_questions = load_extracted_questions(extracted_questions_path)
    
    print(f"Loaded {len(extracted_questions)} extracted questions")
    
    # Process and validate questions
    processed_questions = process_extracted_questions(extracted_questions)
    print(f"Processed {len(processed_questions)} valid questions")
    
    # Initialize question bank
    question_bank = QuestionBank()
    
    # Merge new questions into the main bank
    question_bank = merge_questions(question_bank, processed_questions)
    
    print(f"Total questions in bank: {len(question_bank.questions)}")
    
    # Save updated question bank
    with open("data/question_bank.json", 'w') as f:
        json.dump({
            "questions": [q.__dict__ for q in question_bank.questions],
            "strategies": {k: v.__dict__ for k, v in question_bank.strategies.items()},
            "difficulty_config": question_bank.difficulty_config.__dict__
        }, f, indent=2)
    
    print("Question bank saved to data/question_bank.json")


if __name__ == "__main__":
    main()

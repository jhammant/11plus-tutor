#!/usr/bin/env python3
"""
Generate validated code_words questions for 11+ Tutor.
Each question uses a Caesar cipher and is mathematically verified.
"""

import json
import uuid
import random
import sys
from pathlib import Path
from datetime import datetime

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.database import init_db, Question, SessionLocal

# Common 4-6 letter words for code_words questions
WORDS = [
    # 4-letter words
    "WORD", "MATH", "BOOK", "FISH", "BIRD", "TREE", "HAND", "FACE", "DOOR", "LAKE",
    "FIRE", "WIND", "RAIN", "SNOW", "STAR", "MOON", "GOLD", "PINK", "BLUE", "GRAY",
    "KING", "JUMP", "WALK", "TALK", "PLAY", "READ", "SING", "DRAW", "SWIM", "RIDE",
    "CAMP", "HELP", "LIFT", "PUSH", "PULL", "KICK", "WAVE", "CLAP", "SPIN", "FLIP",
    "BEAR", "DUCK", "FROG", "GOAT", "LION", "WOLF", "DEER", "SEAL", "CRAB", "MOTH",

    # 5-letter words
    "HOUSE", "SMART", "BRAIN", "DANCE", "MUSIC", "LIGHT", "NIGHT", "DREAM", "PEACE",
    "EARTH", "WATER", "PLANT", "FRUIT", "BREAD", "CHAIR", "TABLE", "CLOCK", "PHONE",
    "SMILE", "LAUGH", "THINK", "LEARN", "TEACH", "WRITE", "SPEAK", "SLEEP", "CLIMB",
    "HORSE", "SHEEP", "SNAKE", "WHALE", "TIGER", "ZEBRA", "PANDA", "CAMEL", "MOUSE",
    "CLOUD", "STORM", "FROST", "BEACH", "RIVER", "OCEAN", "MOUNT", "FIELD", "GRASS",

    # 6-letter words
    "TARGET", "FRIEND", "SCHOOL", "FAMILY", "GARDEN", "ANIMAL", "BRIDGE", "CASTLE",
    "FLOWER", "MONKEY", "RABBIT", "DRAGON", "PLANET", "SUMMER", "WINTER", "SPRING",
    "AUTUMN", "ORANGE", "PURPLE", "YELLOW", "SILVER", "GOLDEN", "BRIGHT", "SISTER",
    "BROTHER", "PARENT", "MARKET", "ISLAND", "FOREST", "DESERT", "JUNGLE", "STREAM",
]

def apply_cipher(word: str, shift: int) -> str:
    """Apply Caesar cipher with given shift."""
    result = []
    for c in word.upper():
        if c.isalpha():
            shifted = (ord(c) - ord('A') + shift) % 26
            result.append(chr(shifted + ord('A')))
        else:
            result.append(c)
    return ''.join(result)


def generate_wrong_options(correct: str, shift: int, num_options: int = 4) -> list:
    """Generate plausible but incorrect options."""
    wrong = set()
    word_len = len(correct)

    # Strategy 1: Different shifts
    for s in [-3, -2, -1, 1, 3, 4, 5]:
        if s != shift and s != 0:
            # Apply different shift to get wrong answer
            wrong_word = ''.join(
                chr((ord(c) - ord('A') + s - shift) % 26 + ord('A')) if c.isalpha() else c
                for c in correct
            )
            if wrong_word != correct:
                wrong.add(wrong_word)

    # Strategy 2: Swap some letters
    for _ in range(10):
        chars = list(correct)
        if len(chars) >= 2:
            i, j = random.sample(range(len(chars)), 2)
            chars[i], chars[j] = chars[j], chars[i]
            wrong_word = ''.join(chars)
            if wrong_word != correct:
                wrong.add(wrong_word)

    # Strategy 3: Change one letter
    for i in range(len(correct)):
        for delta in [-1, 1, 2]:
            chars = list(correct)
            new_char = chr((ord(chars[i]) - ord('A') + delta) % 26 + ord('A'))
            chars[i] = new_char
            wrong_word = ''.join(chars)
            if wrong_word != correct:
                wrong.add(wrong_word)

    # Select random subset
    wrong_list = list(wrong)
    random.shuffle(wrong_list)
    return wrong_list[:num_options]


def generate_question(example_word: str, target_word: str, shift: int) -> dict:
    """Generate a single code_words question with validation."""

    # Calculate coded words
    coded_example = apply_cipher(example_word, shift)
    correct_answer = apply_cipher(target_word, shift)

    # Validate lengths match
    assert len(example_word) == len(coded_example), "Example length mismatch"
    assert len(target_word) == len(correct_answer), "Target length mismatch"

    # Verify cipher is consistent
    for i, (orig, coded) in enumerate(zip(example_word, coded_example)):
        actual_shift = (ord(coded) - ord(orig)) % 26
        assert actual_shift == shift, f"Shift inconsistency at position {i}"

    # Generate wrong options
    wrong_options = generate_wrong_options(correct_answer, shift, 4)

    # Build options list (correct answer at random position)
    options = wrong_options[:4]
    correct_index = random.randint(0, 4)
    options.insert(correct_index, correct_answer)

    # Final validation
    assert correct_answer == options[correct_index], "Answer index mismatch"
    assert len(options) == 5, "Should have 5 options"
    assert correct_answer in options, "Answer must be in options"

    # Build question
    question = {
        "id": str(uuid.uuid4()),
        "exam_type": "11plus_gl",
        "subject": "verbal_reasoning",
        "topic": "codes",
        "question_type": "code_words",
        "difficulty": 3 if abs(shift) <= 3 else 4,
        "question_text": f"If {example_word} is coded as {coded_example}, what is the code for {target_word}?",
        "options": options,
        "correct_answer": correct_answer,
        "correct_index": correct_index,
        "explanation": f"Each letter is shifted {'forward' if shift > 0 else 'backward'} by {abs(shift)} place{'s' if abs(shift) != 1 else ''} in the alphabet. Applying this to {target_word}: {' -> '.join(f'{a}->{b}' for a, b in zip(target_word, correct_answer))}, giving {correct_answer}.",
        "created_at": datetime.utcnow().isoformat(),
    }

    return question


def validate_question(q: dict) -> bool:
    """Double-check a question is correct."""
    import re

    text = q['question_text']
    match = re.search(r'If\s+(\w+)\s+is\s+coded\s+as\s+(\w+).*code\s+for\s+(\w+)', text, re.IGNORECASE)
    if not match:
        return False

    example = match.group(1).upper()
    coded = match.group(2).upper()
    target = match.group(3).upper()

    # Extract shift
    if len(example) != len(coded):
        return False

    shifts = [(ord(coded[i]) - ord(example[i])) % 26 for i in range(len(example))]
    if len(set(shifts)) != 1:
        return False

    shift = shifts[0]
    expected_answer = apply_cipher(target, shift)

    return q['correct_answer'].upper() == expected_answer


def generate_questions(count: int = 30) -> list:
    """Generate multiple validated questions."""
    questions = []
    used_pairs = set()  # Avoid duplicates

    shifts = [1, 2, 3, 4, 5, -1, -2, -3, 23, 24, 25]  # Various shifts including negative

    attempts = 0
    while len(questions) < count and attempts < count * 10:
        attempts += 1

        # Pick random words (same length for example and target)
        example = random.choice(WORDS)
        target_options = [w for w in WORDS if len(w) == len(example) and w != example]
        if not target_options:
            continue
        target = random.choice(target_options)

        # Check for duplicate
        pair_key = f"{example}_{target}"
        if pair_key in used_pairs:
            continue
        used_pairs.add(pair_key)

        # Pick random shift
        shift = random.choice(shifts)

        try:
            q = generate_question(example, target, shift)

            # Validate before adding
            if validate_question(q):
                questions.append(q)
                print(f"  Generated: {example} -> {apply_cipher(example, shift)} (shift {shift:+d}), target {target} -> {q['correct_answer']}")
            else:
                print(f"  FAILED validation: {example} -> {target}")
        except Exception as e:
            print(f"  Error generating {example} -> {target}: {e}")

    return questions


def save_to_database(questions: list):
    """Save questions to database."""
    init_db()
    db = SessionLocal()

    added = 0
    for q in questions:
        # Check if already exists
        existing = db.query(Question).filter(Question.id == q['id']).first()
        if existing:
            continue

        question = Question(
            id=q['id'],
            exam_type=q['exam_type'],
            subject=q['subject'],
            topic=q.get('topic'),
            question_type=q['question_type'],
            difficulty=q['difficulty'],
            question_text=q['question_text'],
            options=q['options'],
            correct_answer=q['correct_answer'],
            correct_index=q['correct_index'],
            worked_solution=q.get('explanation'),
        )
        db.add(question)
        added += 1

    db.commit()
    db.close()

    return added


if __name__ == "__main__":
    print("Code Words Question Generator")
    print("=" * 50)

    count = int(sys.argv[1]) if len(sys.argv) > 1 else 30

    print(f"\nGenerating {count} validated questions...")
    questions = generate_questions(count)

    print(f"\nGenerated {len(questions)} valid questions")

    print("\nSaving to database...")
    added = save_to_database(questions)
    print(f"Added {added} new questions to database")

    # Final count
    db = SessionLocal()
    total = db.query(Question).filter(Question.question_type == "code_words").count()
    db.close()
    print(f"\nTotal code_words questions: {total}")

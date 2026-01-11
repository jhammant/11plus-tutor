#!/usr/bin/env python3
"""
Question Generator for 11+ Tutor
Generates mathematically-verified questions for topics where answers can be computed.

This generator creates questions that are GUARANTEED to be correct because
the answers are computed, not guessed.

Usage:
    python scripts/generate_questions.py --type sequences --count 50
    python scripts/generate_questions.py --type arithmetic --count 50
    python scripts/generate_questions.py --all --count 100
"""

import sqlite3
import json
import random
import argparse
import uuid
from typing import List


class QuestionGenerator:
    """Generate mathematically-verified questions."""

    def __init__(self, db_path: str = "elevenplustutor.db"):
        self.db_path = db_path

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def save_question(self, question: dict):
        """Save a question to the database."""
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO questions (
                id, exam_type, subject, topic, question_type, difficulty,
                question_text, options, correct_answer, correct_index,
                marks_available, hint, worked_solution
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            question['id'],
            question.get('exam_type', '11plus_gl'),
            question['subject'],
            question.get('topic', question['question_type']),
            question['question_type'],
            question['difficulty'],
            question['question_text'],
            json.dumps(question['options']),
            question['correct_answer'],
            question['correct_index'],
            question.get('marks_available', 1),
            question.get('hint'),
            question.get('worked_solution')
        ))

        conn.commit()
        conn.close()

    def generate_arithmetic_sequence(self, difficulty: int = 2) -> dict:
        """Generate arithmetic sequence (constant difference)."""
        if difficulty <= 2:
            start = random.randint(1, 20)
            diff = random.randint(2, 7)
            length = 4
        elif difficulty == 3:
            start = random.randint(5, 50)
            diff = random.choice([3, 4, 5, 6, 7, 8, 9, 11, 12, 13])
            length = 5
        else:
            start = random.randint(10, 100)
            diff = random.choice([7, 9, 11, 13, 15, 17, 19])
            length = 5

        sequence = [start + i * diff for i in range(length)]
        answer = sequence[-1] + diff

        wrong = [answer - 1, answer + 1, answer - diff, answer + diff + 1,
                 answer - 2, answer + 2, sequence[-1] + diff - 1]
        wrong = list(set([w for w in wrong if w != answer and w > 0]))[:4]
        random.shuffle(wrong)

        options = wrong[:4] + [answer]
        random.shuffle(options)
        correct_index = options.index(answer)
        sequence_str = ", ".join(str(n) for n in sequence)

        return {
            'id': str(uuid.uuid4()),
            'subject': 'mathematics',
            'question_type': 'sequences',
            'difficulty': difficulty,
            'question_text': f"What comes next in the sequence?\n{sequence_str}, ___",
            'options': [str(o) for o in options],
            'correct_answer': str(answer),
            'correct_index': correct_index,
            'worked_solution': f"This is an arithmetic sequence where each number increases by {diff}.\n{sequence[-1]} + {diff} = {answer}"
        }

    def generate_quadratic_sequence(self, difficulty: int = 3) -> dict:
        """Generate sequence with increasing differences."""
        start = random.randint(1, 10)
        initial_diff = random.randint(1, 4)
        diff_increase = random.randint(1, 3)
        length = 5

        sequence = [start]
        diff = initial_diff
        for _ in range(length - 1):
            sequence.append(sequence[-1] + diff)
            diff += diff_increase

        next_diff = initial_diff + diff_increase * (length - 1)
        answer = sequence[-1] + next_diff

        wrong = [answer - 1, answer + 1, answer - 2, answer + 2,
                 sequence[-1] + next_diff - diff_increase]
        wrong = list(set([w for w in wrong if w != answer and w > 0]))[:4]

        options = wrong[:4] + [answer]
        random.shuffle(options)
        correct_index = options.index(answer)
        sequence_str = ", ".join(str(n) for n in sequence)

        return {
            'id': str(uuid.uuid4()),
            'subject': 'mathematics',
            'question_type': 'sequences',
            'difficulty': difficulty,
            'question_text': f"What comes next in the sequence?\n{sequence_str}, ___",
            'options': [str(o) for o in options],
            'correct_answer': str(answer),
            'correct_index': correct_index,
            'worked_solution': f"The differences increase by {diff_increase} each time.\nNext difference: {next_diff}, so {sequence[-1]} + {next_diff} = {answer}"
        }

    def generate_letter_sequence(self, difficulty: int = 2) -> dict:
        """Generate letter sequence with consistent pattern."""
        start1 = random.randint(0, 20)
        start2 = random.randint(0, 20)
        step1 = random.randint(1, 2) if difficulty <= 2 else random.randint(1, 3)
        step2 = random.randint(1, 2) if difficulty <= 2 else random.randint(1, 3)
        length = 4

        def to_letter(n):
            return chr(65 + (n % 26))

        sequence = []
        for i in range(length):
            sequence.append(to_letter(start1 + i * step1) + to_letter(start2 + i * step2))

        answer = to_letter(start1 + length * step1) + to_letter(start2 + length * step2)

        wrong = [
            to_letter(start1 + length * step1 + 1) + to_letter(start2 + length * step2),
            to_letter(start1 + length * step1) + to_letter(start2 + length * step2 + 1),
            to_letter(start1 + length * step1 - 1) + to_letter(start2 + length * step2),
            to_letter(start1 + (length + 1) * step1) + to_letter(start2 + length * step2),
        ]
        wrong = [w for w in wrong if w != answer][:4]

        options = wrong + [answer]
        random.shuffle(options)
        correct_index = options.index(answer)
        sequence_str = ", ".join(sequence)

        return {
            'id': str(uuid.uuid4()),
            'subject': 'verbal_reasoning',
            'question_type': 'letter_sequences',
            'difficulty': difficulty,
            'question_text': f"What comes next in the sequence?\n{sequence_str}, ___",
            'options': options,
            'correct_answer': answer,
            'correct_index': correct_index,
            'worked_solution': f"First letters advance by {step1}, second by {step2}. Answer: {answer}"
        }

    def generate_addition(self, difficulty: int = 2) -> dict:
        if difficulty <= 2:
            a, b = random.randint(10, 99), random.randint(10, 99)
        else:
            a, b = random.randint(100, 999), random.randint(10, 99)
        answer = a + b
        wrong = list(set([answer - 1, answer + 1, answer - 10, answer + 10]))[:4]
        options = wrong[:4] + [answer]
        random.shuffle(options)
        return {
            'id': str(uuid.uuid4()), 'subject': 'mathematics', 'question_type': 'arithmetic',
            'difficulty': difficulty, 'question_text': f"Calculate: {a} + {b} = ?",
            'options': [str(o) for o in options], 'correct_answer': str(answer),
            'correct_index': options.index(answer), 'worked_solution': f"{a} + {b} = {answer}"
        }

    def generate_multiplication(self, difficulty: int = 2) -> dict:
        if difficulty <= 2:
            a, b = random.randint(2, 12), random.randint(2, 12)
        else:
            a, b = random.randint(10, 25), random.randint(2, 9)
        answer = a * b
        wrong = list(set([answer - 1, answer + 1, answer - a, answer + a]))[:4]
        options = wrong[:4] + [answer]
        random.shuffle(options)
        return {
            'id': str(uuid.uuid4()), 'subject': 'mathematics', 'question_type': 'arithmetic',
            'difficulty': difficulty, 'question_text': f"Calculate: {a} × {b} = ?",
            'options': [str(o) for o in options], 'correct_answer': str(answer),
            'correct_index': options.index(answer), 'worked_solution': f"{a} × {b} = {answer}"
        }

    def generate_sequences(self, count: int = 50) -> List[dict]:
        questions = []
        for _ in range(count):
            qtype = random.choices(['arithmetic', 'quadratic'], weights=[0.6, 0.4])[0]
            difficulty = random.choices([2, 3, 4], weights=[0.4, 0.4, 0.2])[0]
            q = self.generate_arithmetic_sequence(difficulty) if qtype == 'arithmetic' else self.generate_quadratic_sequence(difficulty)
            questions.append(q)
        return questions

    def generate_letter_sequences_batch(self, count: int = 30) -> List[dict]:
        return [self.generate_letter_sequence(random.choice([2, 3])) for _ in range(count)]

    def generate_arithmetic_batch(self, count: int = 50) -> List[dict]:
        questions = []
        for _ in range(count):
            q = random.choice([self.generate_addition, self.generate_multiplication])(random.choice([2, 3]))
            questions.append(q)
        return questions


def main():
    parser = argparse.ArgumentParser(description='Generate verified 11+ questions')
    parser.add_argument('--type', choices=['sequences', 'letter_sequences', 'arithmetic', 'all'], default='all')
    parser.add_argument('--count', type=int, default=50)
    parser.add_argument('--db', default='elevenplustutor.db')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    generator = QuestionGenerator(args.db)
    questions = []

    if args.type in ['sequences', 'all']:
        print(f"Generating {args.count} number sequences...")
        questions.extend(generator.generate_sequences(args.count))
    if args.type in ['letter_sequences', 'all']:
        print(f"Generating {args.count} letter sequences...")
        questions.extend(generator.generate_letter_sequences_batch(args.count))
    if args.type in ['arithmetic', 'all']:
        print(f"Generating {args.count} arithmetic questions...")
        questions.extend(generator.generate_arithmetic_batch(args.count))

    if args.dry_run:
        for q in questions[:5]:
            print(f"\nQ: {q['question_text']}")
            print(f"   Options: {q['options']}")
            print(f"   Answer: {q['correct_answer']}")
        print(f"\nTotal: {len(questions)} questions (not saved)")
    else:
        for q in questions:
            generator.save_question(q)
        print(f"\nSaved {len(questions)} questions to database")


if __name__ == '__main__':
    main()

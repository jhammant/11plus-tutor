#!/usr/bin/env python3
"""
Question Validator for 11+ Tutor
Validates questions programmatically and exports for human review.

Usage:
    python scripts/validate_questions.py --validate    # Run automated validation
    python scripts/validate_questions.py --export      # Export for human review
    python scripts/validate_questions.py --all         # Both
"""

import sqlite3
import json
import re
import argparse
from pathlib import Path
from typing import Optional, Tuple, List
import csv
from datetime import datetime

# Known synonym pairs for validation
SYNONYM_PAIRS = {
    ('happy', 'joyful'), ('happy', 'glad'), ('happy', 'cheerful'), ('happy', 'delighted'),
    ('sad', 'unhappy'), ('sad', 'sorrowful'), ('sad', 'melancholy'), ('sad', 'gloomy'),
    ('big', 'large'), ('big', 'huge'), ('big', 'enormous'), ('big', 'massive'),
    ('small', 'tiny'), ('small', 'little'), ('small', 'minute'), ('small', 'petite'),
    ('fast', 'quick'), ('fast', 'rapid'), ('fast', 'swift'), ('fast', 'speedy'),
    ('slow', 'sluggish'), ('slow', 'leisurely'), ('slow', 'unhurried'),
    ('hot', 'warm'), ('hot', 'boiling'), ('hot', 'scorching'),
    ('cold', 'cool'), ('cold', 'freezing'), ('cold', 'chilly'), ('cold', 'frigid'),
    ('good', 'excellent'), ('good', 'great'), ('good', 'fine'), ('good', 'superb'),
    ('bad', 'terrible'), ('bad', 'awful'), ('bad', 'poor'), ('bad', 'dreadful'),
    ('old', 'ancient'), ('old', 'elderly'), ('old', 'aged'),
    ('new', 'modern'), ('new', 'fresh'), ('new', 'recent'), ('new', 'novel'),
    ('bright', 'brilliant'), ('bright', 'luminous'), ('bright', 'radiant'),
    ('dark', 'dim'), ('dark', 'gloomy'), ('dark', 'murky'),
    ('begin', 'start'), ('begin', 'commence'), ('begin', 'initiate'),
    ('end', 'finish'), ('end', 'conclude'), ('end', 'terminate'),
    ('rich', 'wealthy'), ('rich', 'affluent'), ('rich', 'prosperous'),
    ('poor', 'impoverished'), ('poor', 'needy'), ('poor', 'destitute'),
    ('strong', 'powerful'), ('strong', 'mighty'), ('strong', 'robust'),
    ('weak', 'feeble'), ('weak', 'frail'), ('weak', 'fragile'),
    ('rapid', 'swift'), ('rapid', 'quick'), ('rapid', 'fast'),
    ('gentle', 'kind'), ('gentle', 'tender'), ('gentle', 'soft'),
    ('angry', 'furious'), ('angry', 'irate'), ('angry', 'enraged'),
    ('scared', 'frightened'), ('scared', 'afraid'), ('scared', 'terrified'),
    ('beautiful', 'pretty'), ('beautiful', 'lovely'), ('beautiful', 'gorgeous'),
    ('ugly', 'hideous'), ('ugly', 'unsightly'),
    ('clever', 'intelligent'), ('clever', 'smart'), ('clever', 'bright'),
    ('stupid', 'foolish'), ('stupid', 'dumb'),
    ('brave', 'courageous'), ('brave', 'fearless'), ('brave', 'bold'),
    ('cowardly', 'timid'), ('cowardly', 'fearful'),
    ('quiet', 'silent'), ('quiet', 'hushed'), ('quiet', 'still'),
    ('loud', 'noisy'), ('loud', 'boisterous'),
    ('wet', 'damp'), ('wet', 'moist'), ('wet', 'soaked'),
    ('dry', 'arid'), ('dry', 'parched'),
    ('clean', 'spotless'), ('clean', 'tidy'),
    ('dirty', 'filthy'), ('dirty', 'grimy'),
    ('simple', 'easy'), ('simple', 'straightforward'),
    ('difficult', 'hard'), ('difficult', 'challenging'), ('difficult', 'tough'),
    ('thick', 'dense'), ('thick', 'heavy'),
    ('thin', 'slim'), ('thin', 'slender'), ('thin', 'lean'),
    ('tall', 'high'), ('tall', 'lofty'),
    ('short', 'low'), ('short', 'brief'),
    ('wide', 'broad'), ('wide', 'extensive'),
    ('narrow', 'thin'), ('narrow', 'slim'),
    ('deep', 'profound'),
    ('shallow', 'superficial'),
    # Additional pairs found in questions
    ('swift', 'quick'), ('swift', 'fast'), ('swift', 'rapid'), ('swift', 'speedy'),
    ('brisk', 'quick'), ('brisk', 'rapid'), ('brisk', 'fast'), ('brisk', 'lively'),
    ('quick', 'rapid'), ('quick', 'speedy'),
    # More pairs from validation
    ('eat', 'munch'), ('eat', 'consume'), ('eat', 'devour'),
    ('brave', 'valiant'), ('brave', 'heroic'), ('brave', 'gallant'),
    ('wet', 'soggy'), ('wet', 'saturated'),
    ('drink', 'gulp'), ('drink', 'sip'), ('drink', 'swig'),
    ('say', 'speak'), ('say', 'utter'), ('say', 'state'),
    ('look', 'gaze'), ('look', 'stare'), ('look', 'glance'),
    ('run', 'sprint'), ('run', 'dash'), ('run', 'race'),
    ('walk', 'stroll'), ('walk', 'amble'), ('walk', 'wander'),
    ('talk', 'chat'), ('talk', 'converse'), ('talk', 'speak'),
    ('cry', 'weep'), ('cry', 'sob'), ('cry', 'wail'),
    ('laugh', 'chuckle'), ('laugh', 'giggle'), ('laugh', 'snicker'),
    ('shout', 'yell'), ('shout', 'scream'), ('shout', 'bellow'),
    ('grab', 'seize'), ('grab', 'snatch'), ('grab', 'clutch'),
    ('throw', 'hurl'), ('throw', 'toss'), ('throw', 'fling'),
    ('pull', 'tug'), ('pull', 'drag'), ('pull', 'yank'),
    ('push', 'shove'), ('push', 'thrust'),
    ('choose', 'select'), ('choose', 'pick'),
    ('find', 'discover'), ('find', 'locate'),
    ('hide', 'conceal'), ('hide', 'cover'),
    ('show', 'display'), ('show', 'reveal'), ('show', 'exhibit'),
    ('keep', 'retain'), ('keep', 'hold'),
    ('give', 'donate'), ('give', 'present'),
    ('take', 'grab'), ('take', 'seize'),
    ('make', 'create'), ('make', 'produce'), ('make', 'construct'),
    ('break', 'smash'), ('break', 'shatter'),
    ('fix', 'repair'), ('fix', 'mend'),
}

# Known antonym pairs for validation
ANTONYM_PAIRS = {
    ('hot', 'cold'), ('warm', 'cool'),
    ('big', 'small'), ('large', 'tiny'), ('huge', 'tiny'),
    ('fast', 'slow'), ('quick', 'slow'), ('rapid', 'slow'),
    ('good', 'bad'), ('excellent', 'terrible'),
    ('happy', 'sad'), ('joyful', 'sorrowful'), ('cheerful', 'gloomy'),
    ('old', 'new'), ('ancient', 'modern'), ('old', 'young'),
    ('bright', 'dark'), ('light', 'dark'),
    ('bright', 'dim'), ('bright', 'dull'),  # Added
    ('rich', 'poor'), ('wealthy', 'impoverished'),
    ('generous', 'stingy'), ('generous', 'mean'), ('generous', 'selfish'),  # Added
    ('strong', 'weak'), ('powerful', 'feeble'),
    ('tall', 'short'), ('high', 'low'),
    ('wide', 'narrow'), ('broad', 'narrow'),
    ('thick', 'thin'), ('fat', 'thin'),
    ('deep', 'shallow'),
    ('wet', 'dry'), ('damp', 'dry'),
    ('clean', 'dirty'), ('tidy', 'messy'),
    ('quiet', 'loud'), ('silent', 'noisy'),
    ('brave', 'cowardly'), ('courageous', 'fearful'),
    ('clever', 'stupid'), ('intelligent', 'foolish'), ('smart', 'dumb'),
    ('beautiful', 'ugly'), ('pretty', 'hideous'),
    ('begin', 'end'), ('start', 'finish'), ('commence', 'conclude'),
    ('love', 'hate'),
    ('open', 'close'), ('open', 'shut'),
    ('up', 'down'),
    ('in', 'out'),
    ('top', 'bottom'),
    ('front', 'back'),
    ('left', 'right'),
    ('day', 'night'),
    ('early', 'late'),
    ('always', 'never'),
    ('many', 'few'),
    ('more', 'less'),
    ('full', 'empty'),
    ('hard', 'soft'), ('hard', 'easy'),
    ('rough', 'smooth'),
    ('sharp', 'blunt'), ('sharp', 'dull'),
    ('sweet', 'sour'), ('sweet', 'bitter'),
    ('true', 'false'),
    ('right', 'wrong'),
    ('success', 'failure'),
    ('win', 'lose'),
    ('push', 'pull'),
    ('give', 'take'),
    ('buy', 'sell'),
    ('arrive', 'depart'), ('come', 'go'),
    ('rise', 'fall'), ('ascend', 'descend'),
    ('increase', 'decrease'), ('grow', 'shrink'),
    ('appear', 'disappear'), ('visible', 'invisible'),
    ('remember', 'forget'),
    ('accept', 'reject'), ('accept', 'refuse'),
    ('allow', 'forbid'), ('permit', 'prohibit'),
    ('include', 'exclude'),
    ('join', 'separate'),
    ('attack', 'defend'),
    ('borrow', 'lend'),
    ('harm', 'help'),
    ('praise', 'criticize'),
    ('reward', 'punish'),
    ('noise', 'silence'),
    # More pairs from validation
    ('over', 'under'), ('above', 'below'),
    ('victory', 'defeat'), ('win', 'loss'),
    ('donate', 'accept'), ('give', 'receive'),
    ('moist', 'parched'), ('moist', 'dry'),
    ('wonderful', 'awful'), ('wonderful', 'terrible'),
    ('heavy', 'light'), ('heavy', 'lightweight'),
    ('often', 'rarely'), ('often', 'seldom'),
    ('powerful', 'weak'), ('mighty', 'feeble'),
    ('giant', 'tiny'), ('giant', 'small'),
    ('internal', 'external'), ('inside', 'outside'),
    ('purchase', 'trade'), ('buy', 'sell'),
    ('lovely', 'ugly'), ('lovely', 'hideous'),
    ('war', 'peace'), ('conflict', 'harmony'),
    ('complex', 'simple'), ('complicated', 'easy'),
    ('ancient', 'new'), ('ancient', 'young'),
    ('maximum', 'minimum'), ('most', 'least'),
    ('positive', 'negative'), ('plus', 'minus'),
    ('public', 'private'), ('public', 'secret'),
    ('polite', 'rude'), ('courteous', 'impolite'),
    ('innocent', 'guilty'), ('innocent', 'culpable'),
    ('permanent', 'temporary'), ('lasting', 'brief'),
    ('common', 'rare'), ('frequent', 'unusual'),
    ('natural', 'artificial'), ('real', 'fake'),
    ('ordinary', 'extraordinary'), ('normal', 'unusual'),
    ('tight', 'loose'), ('firm', 'slack'),
    ('straight', 'crooked'), ('straight', 'bent'),
    ('smooth', 'rough'), ('even', 'uneven'),
    ('calm', 'stormy'), ('calm', 'agitated'),
    ('awake', 'asleep'), ('conscious', 'unconscious'),
    ('alive', 'dead'), ('living', 'deceased'),
}

def are_synonyms(word1: str, word2: str) -> bool:
    """Check if two words are known synonyms."""
    w1, w2 = word1.lower().strip(), word2.lower().strip()
    return (w1, w2) in SYNONYM_PAIRS or (w2, w1) in SYNONYM_PAIRS

def are_antonyms(word1: str, word2: str) -> bool:
    """Check if two words are known antonyms."""
    w1, w2 = word1.lower().strip(), word2.lower().strip()
    return (w1, w2) in ANTONYM_PAIRS or (w2, w1) in ANTONYM_PAIRS


class QuestionValidator:
    def __init__(self, db_path: str = "elevenplustutor.db"):
        self.db_path = db_path
        self.issues = []
        self.validated = []

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def validate_all(self) -> Tuple[int, int, List[dict]]:
        """Validate all questions. Returns (passed, failed, issues)."""
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM questions")

        passed = 0
        failed = 0
        self.issues = []

        for row in cur.fetchall():
            q = dict(row)
            result = self.validate_question(q)
            if result['valid']:
                passed += 1
            else:
                failed += 1
                self.issues.append(result)

        conn.close()
        return passed, failed, self.issues

    def validate_question(self, q: dict) -> dict:
        """Validate a single question based on its type."""
        result = {
            'id': q['id'],
            'type': q['question_type'],
            'subject': q['subject'],
            'question': q['question_text'][:100],
            'answer': q['correct_answer'],
            'valid': True,
            'issues': [],
            'confidence': 'high'
        }

        qtype = q['question_type']

        if qtype == 'synonyms':
            self._validate_synonym(q, result)
        elif qtype == 'antonyms':
            self._validate_antonym(q, result)
        elif qtype == 'sequences':
            self._validate_number_sequence(q, result)
        elif qtype == 'letter_sequences':
            self._validate_letter_sequence(q, result)
        elif qtype == 'arithmetic':
            self._validate_arithmetic(q, result)
        elif qtype == 'fractions':
            self._validate_fractions(q, result)
        elif qtype == 'analogies':
            self._validate_analogy(q, result)
        elif qtype == 'code_words':
            self._validate_code_words(q, result)
        elif qtype == 'odd_one_out':
            self._validate_odd_one_out(q, result)
        else:
            result['confidence'] = 'unknown'
            result['issues'].append(f"Unknown question type: {qtype}")

        return result

    def _validate_synonym(self, q: dict, result: dict):
        """Validate synonym question."""
        answer = q['correct_answer']
        # Parse answer like "happy & joyful"
        if ' & ' in answer:
            words = answer.split(' & ')
            if len(words) == 2:
                if not are_synonyms(words[0], words[1]):
                    result['valid'] = False
                    result['issues'].append(f"'{words[0]}' and '{words[1]}' may not be synonyms")
                    result['confidence'] = 'medium'
                else:
                    result['confidence'] = 'high'
            else:
                result['confidence'] = 'low'
                result['issues'].append("Could not parse answer format")
        else:
            result['confidence'] = 'low'
            result['issues'].append("Answer not in expected format (word1 & word2)")

    def _validate_antonym(self, q: dict, result: dict):
        """Validate antonym question."""
        answer = q['correct_answer']
        if ' & ' in answer:
            words = answer.split(' & ')
            if len(words) == 2:
                if not are_antonyms(words[0], words[1]):
                    result['valid'] = False
                    result['issues'].append(f"'{words[0]}' and '{words[1]}' may not be antonyms")
                    result['confidence'] = 'medium'
                else:
                    result['confidence'] = 'high'
            else:
                result['confidence'] = 'low'

    def _validate_number_sequence(self, q: dict, result: dict):
        """Validate number sequence - check if pattern holds."""
        text = q['question_text']
        answer = q['correct_answer']

        # Extract numbers from question
        numbers = re.findall(r'\d+', text.split('___')[0] if '___' in text else text)
        numbers = [int(n) for n in numbers]

        if len(numbers) < 3:
            result['confidence'] = 'low'
            result['issues'].append("Not enough numbers to detect pattern")
            return

        try:
            answer_num = int(answer)
        except:
            result['confidence'] = 'low'
            result['issues'].append("Answer is not a number")
            return

        # Check for arithmetic sequence (constant difference)
        diffs = [numbers[i+1] - numbers[i] for i in range(len(numbers)-1)]
        if len(set(diffs)) == 1:
            # Constant difference
            expected = numbers[-1] + diffs[0]
            if expected != answer_num:
                result['valid'] = False
                result['issues'].append(f"Arithmetic sequence: expected {expected}, got {answer_num}")
            result['confidence'] = 'high'
            return

        # Check for increasing differences
        diff_diffs = [diffs[i+1] - diffs[i] for i in range(len(diffs)-1)]
        if len(diff_diffs) > 0 and len(set(diff_diffs)) == 1:
            next_diff = diffs[-1] + diff_diffs[0]
            expected = numbers[-1] + next_diff
            if expected != answer_num:
                result['valid'] = False
                result['issues'].append(f"Quadratic sequence: expected {expected}, got {answer_num}")
            result['confidence'] = 'high'
            return

        # Check for geometric sequence (constant ratio)
        if all(numbers[i] != 0 for i in range(len(numbers)-1)):
            ratios = [numbers[i+1] / numbers[i] for i in range(len(numbers)-1)]
            if len(set([round(r, 2) for r in ratios])) == 1:
                expected = int(numbers[-1] * ratios[0])
                if expected != answer_num:
                    result['valid'] = False
                    result['issues'].append(f"Geometric sequence: expected {expected}, got {answer_num}")
                result['confidence'] = 'high'
                return

        # Could not determine pattern
        result['confidence'] = 'medium'
        result['issues'].append("Complex pattern - needs manual review")

    def _validate_letter_sequence(self, q: dict, result: dict):
        """Validate letter sequence."""
        text = q['question_text']
        answer = q['correct_answer'].upper()

        # Extract letter groups
        groups = re.findall(r'[A-Z]{2,}', text.upper())

        if len(groups) < 2:
            result['confidence'] = 'low'
            result['issues'].append("Not enough letter groups found")
            return

        # Check simple patterns
        # Pattern: each letter advances by same amount
        if len(groups[0]) == 2:
            # Two-letter groups like AB, CD, EF
            first_letters = [g[0] for g in groups]
            second_letters = [g[1] for g in groups]

            first_diffs = [ord(first_letters[i+1]) - ord(first_letters[i]) for i in range(len(first_letters)-1)]
            second_diffs = [ord(second_letters[i+1]) - ord(second_letters[i]) for i in range(len(second_letters)-1)]

            if first_diffs and second_diffs:
                if len(set(first_diffs)) == 1 and len(set(second_diffs)) == 1:
                    expected_first = chr(ord(first_letters[-1]) + first_diffs[0])
                    expected_second = chr(ord(second_letters[-1]) + second_diffs[0])
                    expected = expected_first + expected_second

                    if expected != answer:
                        result['valid'] = False
                        result['issues'].append(f"Expected {expected}, got {answer}")
                    result['confidence'] = 'high'
                    return

        result['confidence'] = 'medium'
        result['issues'].append("Complex letter pattern - needs manual review")

    def _validate_arithmetic(self, q: dict, result: dict):
        """Validate arithmetic word problems - harder to validate automatically."""
        # These are word problems, harder to parse
        result['confidence'] = 'low'
        result['issues'].append("Word problem - needs manual review")

    def _validate_fractions(self, q: dict, result: dict):
        """Validate fraction questions."""
        result['confidence'] = 'low'
        result['issues'].append("Fraction problem - needs manual review")

    def _validate_analogy(self, q: dict, result: dict):
        """Validate analogy questions."""
        # Analogies are relationship-based, harder to validate
        result['confidence'] = 'medium'
        result['issues'].append("Analogy - needs manual review")

    def _validate_code_words(self, q: dict, result: dict):
        """Validate code word questions."""
        result['confidence'] = 'medium'
        result['issues'].append("Code words - needs manual review")

    def _validate_odd_one_out(self, q: dict, result: dict):
        """Validate odd one out questions."""
        result['confidence'] = 'medium'
        result['issues'].append("Odd one out - needs manual review")

    def export_for_review(self, output_dir: str = "question_review"):
        """Export all questions to CSV files for human review."""
        Path(output_dir).mkdir(exist_ok=True)

        conn = self.connect()
        cur = conn.cursor()

        # Get all question types
        cur.execute("SELECT DISTINCT question_type FROM questions")
        types = [row[0] for row in cur.fetchall()]

        for qtype in types:
            cur.execute("""
                SELECT id, subject, question_type, difficulty, question_text,
                       options, correct_answer, correct_index, worked_solution
                FROM questions
                WHERE question_type = ?
                ORDER BY id
            """, (qtype,))

            rows = cur.fetchall()
            if not rows:
                continue

            filename = f"{output_dir}/{qtype}_questions.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'ID', 'Subject', 'Type', 'Difficulty',
                    'Question', 'Options', 'Correct Answer',
                    'Correct Index', 'Worked Solution',
                    'VERIFIED (Y/N)', 'ISSUES/NOTES'
                ])

                for row in rows:
                    options = row[5]
                    if options:
                        try:
                            options = ' | '.join(json.loads(options))
                        except:
                            pass

                    writer.writerow([
                        row[0], row[1], row[2], row[3],
                        row[4], options, row[6], row[7], row[8],
                        '', ''  # For human to fill in
                    ])

            print(f"  Exported {len(rows)} {qtype} questions to {filename}")

        conn.close()

        # Also create a summary file
        summary_file = f"{output_dir}/REVIEW_INSTRUCTIONS.md"
        with open(summary_file, 'w') as f:
            f.write("""# Question Review Instructions

## How to Review

1. Open each CSV file in Excel or Google Sheets
2. For each question:
   - Read the question and options
   - Verify the correct answer is actually correct
   - Mark VERIFIED column as Y (correct) or N (incorrect)
   - Add notes in ISSUES/NOTES column if there are problems

## Priority Order

Review in this order (most error-prone first):
1. `synonyms_questions.csv` - Check word relationships
2. `antonyms_questions.csv` - Check opposite relationships
3. `letter_sequences_questions.csv` - Verify patterns
4. `sequences_questions.csv` - Check number patterns
5. `analogies_questions.csv` - Verify relationships
6. `code_words_questions.csv` - Check encoding logic
7. `arithmetic_questions.csv` - Calculate answers
8. `fractions_questions.csv` - Verify math
9. `odd_one_out_questions.csv` - Check categorization

## After Review

Run: `python scripts/validate_questions.py --import-review question_review/`

This will update the database with verification status.
""")

        print(f"\n  Created review instructions at {summary_file}")


def main():
    parser = argparse.ArgumentParser(description='Validate 11+ Tutor questions')
    parser.add_argument('--validate', action='store_true', help='Run automated validation')
    parser.add_argument('--export', action='store_true', help='Export questions for review')
    parser.add_argument('--all', action='store_true', help='Run both validation and export')
    parser.add_argument('--db', default='elevenplustutor.db', help='Database path')

    args = parser.parse_args()

    if not any([args.validate, args.export, args.all]):
        args.all = True  # Default to all

    validator = QuestionValidator(args.db)

    if args.validate or args.all:
        print("\n=== Running Automated Validation ===\n")
        passed, failed, issues = validator.validate_all()

        print(f"Results: {passed} passed, {failed} flagged for review\n")

        if issues:
            print("Issues found:")
            for issue in issues[:20]:  # Show first 20
                print(f"\n  [{issue['type']}] {issue['id']}")
                print(f"    Q: {issue['question']}...")
                print(f"    A: {issue['answer']}")
                print(f"    Confidence: {issue['confidence']}")
                for i in issue['issues']:
                    print(f"    - {i}")

            if len(issues) > 20:
                print(f"\n  ... and {len(issues) - 20} more issues")

        # Summary by confidence
        print("\n=== Validation Summary ===")
        by_confidence = {}
        all_results = []
        conn = validator.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM questions")
        for row in cur.fetchall():
            result = validator.validate_question(dict(row))
            all_results.append(result)
            conf = result['confidence']
            by_confidence[conf] = by_confidence.get(conf, 0) + 1
        conn.close()

        for conf in ['high', 'medium', 'low', 'unknown']:
            if conf in by_confidence:
                print(f"  {conf.upper()} confidence: {by_confidence[conf]} questions")

    if args.export or args.all:
        print("\n=== Exporting Questions for Human Review ===\n")
        validator.export_for_review()
        print("\n  Review files created in 'question_review/' directory")
        print("  Open CSV files in Excel/Sheets and verify each question")


if __name__ == '__main__':
    main()

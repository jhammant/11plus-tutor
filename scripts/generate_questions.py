#!/usr/bin/env python3
"""
Question Generator
Generate practice questions using local LLM (LM Studio / Ollama)
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from openai import OpenAI
except ImportError:
    print("Installing openai...")
    os.system("pip install openai")
    from openai import OpenAI


@dataclass
class GeneratedQuestion:
    """A generated question"""
    id: str
    exam_type: str
    subject: str
    question_type: str
    difficulty: int
    question_text: str
    options: List[str]
    correct_answer: str
    correct_index: int
    explanation: str
    created_at: str


# Question type templates - use $difficulty$ as placeholder to avoid format() conflicts
VR_TEMPLATES = {
    "synonyms": {
        "instruction": "Find two words, one from each group, that are closest in meaning.",
        "example": "(happy, sad, angry) (joyful, upset, calm) → happy, joyful",
        "prompt": """Generate a synonyms question for 11+ Verbal Reasoning.

Create two groups of 3 words each. One word from group 1 should have a synonym in group 2.
Difficulty: $difficulty$/5 (1=common words, 5=advanced vocabulary)

Respond with ONLY valid JSON, no other text:
{
    "question": "Find two words, one from each group, that are closest in meaning.\\n(word1, word2, word3) (word4, word5, word6)",
    "options": ["word1 & word4", "word1 & word5", "word2 & word4", "word2 & word6", "word3 & word5"],
    "correct_index": 0,
    "correct_answer": "word1 & word4",
    "explanation": "These words are synonyms because..."
}

Replace word1-word6 with actual words. Make sure correct_index matches the position of correct_answer in options (0-indexed)."""
    },

    "antonyms": {
        "instruction": "Find two words, one from each group, that are most opposite in meaning.",
        "example": "(hot, warm, tepid) (cold, cool, freezing) → hot, freezing",
        "prompt": """Generate an antonyms question for 11+ Verbal Reasoning.

Create two groups of 3 words each. One word from group 1 should have an antonym in group 2.
Difficulty: $difficulty$/5 (1=common words, 5=advanced vocabulary)

Respond with ONLY valid JSON, no other text:
{
    "question": "Find two words, one from each group, that are most opposite in meaning.\\n(word1, word2, word3) (word4, word5, word6)",
    "options": ["word1 & word4", "word1 & word5", "word2 & word4", "word2 & word6", "word3 & word5"],
    "correct_index": 0,
    "correct_answer": "word1 & word4",
    "explanation": "These words are antonyms because..."
}

Replace word1-word6 with actual words. Make sure correct_index matches the position of correct_answer in options (0-indexed)."""
    },

    "analogies": {
        "instruction": "Complete the analogy.",
        "example": "Bird is to nest as bee is to ___ → hive",
        "prompt": """Generate an analogy question for 11+ Verbal Reasoning.

Create a word relationship puzzle: A is to B as C is to ___
Difficulty: $difficulty$/5 (1=simple relationships, 5=complex abstract relationships)

Respond with ONLY valid JSON, no other text:
{
    "question": "WORD1 is to WORD2 as WORD3 is to ___",
    "options": ["option1", "option2", "option3", "option4", "option5"],
    "correct_index": 0,
    "correct_answer": "option1",
    "explanation": "The relationship is..."
}

Use actual words. Make sure correct_index matches the position of correct_answer in options (0-indexed)."""
    },

    "odd_one_out": {
        "instruction": "Find the odd one out.",
        "example": "apple, banana, carrot, orange, grape → carrot (not a fruit)",
        "prompt": """Generate an odd one out question for 11+ Verbal Reasoning.

Create a list of 5 words where 4 share a common property and 1 is different.
Difficulty: $difficulty$/5 (1=obvious categories, 5=subtle distinctions)

Respond with ONLY valid JSON, no other text:
{
    "question": "Find the odd one out:\\nword1, word2, word3, word4, word5",
    "options": ["word1", "word2", "word3", "word4", "word5"],
    "correct_index": 2,
    "correct_answer": "word3",
    "explanation": "word3 is the odd one out because the others are all X, but word3 is Y"
}

Use actual words. Make sure correct_index matches the position of correct_answer in options (0-indexed)."""
    },

    "code_words": {
        "instruction": "Work out the code.",
        "example": "If CAT = DBU, then DOG = ? → EPH (each letter +1)",
        "prompt": """Generate a code words question for 11+ Verbal Reasoning.

Create a letter code puzzle where letters are shifted or transformed by a rule.
Difficulty: $difficulty$/5 (1=simple +1/-1 shifts, 5=complex patterns)

Respond with ONLY valid JSON, no other text:
{
    "question": "If WORD is coded as CODE, what is the code for TARGET?",
    "options": ["option1", "option2", "option3", "option4", "option5"],
    "correct_index": 0,
    "correct_answer": "option1",
    "explanation": "The rule is: each letter is shifted by N in the alphabet"
}

Use actual words and codes. Make sure correct_index matches the position of correct_answer in options (0-indexed)."""
    },

    "letter_sequences": {
        "instruction": "Find the next letters in the sequence.",
        "example": "AB, CD, EF, GH, ___ → IJ",
        "prompt": """Generate a letter sequence question for 11+ Verbal Reasoning.

Create a sequence of letter pairs/groups following a pattern.
Difficulty: $difficulty$/5 (1=simple alphabetical, 5=complex patterns)

Respond with ONLY valid JSON, no other text:
{
    "question": "What comes next in the sequence?\\nAB, CD, EF, GH, ___",
    "options": ["IJ", "HI", "JK", "GI", "IK"],
    "correct_index": 0,
    "correct_answer": "IJ",
    "explanation": "The pattern is: each pair advances by 2 letters"
}

Create an actual sequence. Make sure correct_index matches the position of correct_answer in options (0-indexed)."""
    },

    "hidden_words": {
        "instruction": "Find the hidden word.",
        "example": "The car rotates slowly. → rot (caROTates)",
        "prompt": """Generate a hidden word question for 11+ Verbal Reasoning.

Create a sentence with a 4-letter word hidden across the boundary of two adjacent words.
Difficulty: $difficulty$/5 (1=common hidden words, 5=harder to spot)

Respond with ONLY valid JSON, no other text:
{
    "question": "Find the four-letter word hidden in this sentence:\\nThe car rotates slowly.",
    "options": ["rota", "slow", "cart", "owls", "trot"],
    "correct_index": 0,
    "correct_answer": "rota",
    "explanation": "The hidden word 'rota' spans 'caR OTAtes'"
}

Create an actual sentence with a hidden word. Make sure correct_index matches the position of correct_answer in options (0-indexed)."""
    },

    "compound_words": {
        "instruction": "Find the word that completes both compound words.",
        "example": "sun___ ___rise = sunrise, sunrise... wait that's wrong. Try: book___ ___worm = bookWORM, WORMhole? No...",
        "prompt": """Generate a compound word question for 11+ Verbal Reasoning.

Find a word X that makes: WORD1 + X = compound word AND X + WORD2 = compound word
Example: snow___ ___storm → BALL makes snowBALL and BALLstorm? No. Try: fire___ ___place? No...
Correct example: sun___ ___burn → LIGHT? sunLIGHT and LIGHTburn? No... Let me think: foot___ ___note = BALL? No.
Actually: sun___ ___flower works! sunFLOWER and FLOWERbed? No that's different second word.

Difficulty: $difficulty$/5

Respond with ONLY valid JSON, no other text:
{
    "question": "Find the word that completes both compound words:\\nFIRST___ ___SECOND",
    "options": ["answer", "wrong1", "wrong2", "wrong3", "wrong4"],
    "correct_index": 0,
    "correct_answer": "answer",
    "explanation": "FIRST + answer = FIRSTanswer (compound word), answer + SECOND = answerSECOND (compound word)"
}

Make sure BOTH compound words are real! Make sure correct_index matches the position of correct_answer in options (0-indexed)."""
    },
}

MATHS_TEMPLATES = {
    "arithmetic": {
        "prompt": """Generate an arithmetic word problem for 11+ Mathematics.

Difficulty: $difficulty$/5 (1=single operation, 5=multi-step with fractions/percentages)
Topics: addition, subtraction, multiplication, division, fractions, percentages

Respond with ONLY valid JSON, no other text:
{
    "question": "A word problem involving arithmetic...",
    "options": ["42", "38", "45", "40", "36"],
    "correct_index": 0,
    "correct_answer": "42",
    "explanation": "Step by step solution..."
}

Use actual numbers. Make sure correct_index matches the position of correct_answer in options (0-indexed)."""
    },

    "fractions": {
        "prompt": """Generate a fractions question for 11+ Mathematics.

Difficulty: $difficulty$/5
Include: equivalent fractions, adding, subtracting, or comparing fractions

Respond with ONLY valid JSON, no other text:
{
    "question": "A question about fractions...",
    "options": ["1/2", "1/4", "3/4", "2/3", "1/3"],
    "correct_index": 0,
    "correct_answer": "1/2",
    "explanation": "Step by step solution..."
}

Use actual fractions. Make sure correct_index matches the position of correct_answer in options (0-indexed)."""
    },

    "sequences": {
        "prompt": """Generate a number sequences question for 11+ Mathematics.

Difficulty: $difficulty$/5 (1=simple +n patterns, 5=quadratic or complex)

Respond with ONLY valid JSON, no other text:
{
    "question": "What comes next in the sequence?\\n2, 5, 8, 11, ___",
    "options": ["14", "13", "15", "12", "16"],
    "correct_index": 0,
    "correct_answer": "14",
    "explanation": "The pattern is: add 3 each time. 11 + 3 = 14"
}

Create an actual number sequence. Make sure correct_index matches the position of correct_answer in options (0-indexed)."""
    },
}


class QuestionGenerator:
    """Generate questions using LLM"""

    def __init__(
        self,
        host: str = "http://localhost:1234/v1",
        api_key: str = "lm-studio",
        model: str = "local-model"
    ):
        self.client = OpenAI(base_url=host, api_key=api_key)
        self.model = model

    def generate(
        self,
        subject: str,
        question_type: str,
        difficulty: int = 3,
        count: int = 1
    ) -> List[GeneratedQuestion]:
        """Generate questions"""

        questions = []

        # Get template
        if subject == "verbal_reasoning":
            templates = VR_TEMPLATES
        elif subject == "mathematics":
            templates = MATHS_TEMPLATES
        else:
            print(f"Unknown subject: {subject}")
            return []

        if question_type not in templates:
            print(f"Unknown question type: {question_type}")
            print(f"Available: {list(templates.keys())}")
            return []

        template = templates[question_type]
        prompt = template["prompt"].replace("$difficulty$", str(difficulty))

        for i in range(count):
            print(f"Generating {question_type} question {i+1}/{count}...")

            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert 11+ exam question writer. Generate high-quality, age-appropriate questions. Always respond with valid JSON only, no other text."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8,
                    max_tokens=500,
                )

                content = response.choices[0].message.content.strip()

                # Try to extract JSON from response
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]

                data = json.loads(content)

                question = GeneratedQuestion(
                    id=str(uuid.uuid4()),
                    exam_type="11plus_gl",
                    subject=subject,
                    question_type=question_type,
                    difficulty=difficulty,
                    question_text=data["question"],
                    options=data["options"],
                    correct_answer=data["correct_answer"],
                    correct_index=data["correct_index"],
                    explanation=data["explanation"],
                    created_at=datetime.now().isoformat(),
                )

                questions.append(question)
                print(f"  ✓ Generated: {question.question_text[:50]}...")

            except json.JSONDecodeError as e:
                print(f"  ✗ Failed to parse JSON: {e}")
                print(f"    Response was: {content[:200]}...")
            except Exception as e:
                print(f"  ✗ Error: {e}")

        return questions


def save_questions(questions: List[GeneratedQuestion], output_dir: Path):
    """Save questions to JSON files"""
    output_dir.mkdir(parents=True, exist_ok=True)

    for q in questions:
        filepath = output_dir / f"{q.subject}" / f"{q.question_type}" / f"{q.id}.json"
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w') as f:
            json.dump(asdict(q), f, indent=2)

    # Also save a combined file
    combined_path = output_dir / "all_questions.json"
    existing = []
    if combined_path.exists():
        with open(combined_path) as f:
            existing = json.load(f)

    existing.extend([asdict(q) for q in questions])

    with open(combined_path, 'w') as f:
        json.dump(existing, f, indent=2)

    print(f"\nSaved {len(questions)} questions to {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Generate 11+ practice questions")
    parser.add_argument("--subject", default="verbal_reasoning",
                        choices=["verbal_reasoning", "mathematics"])
    parser.add_argument("--type", dest="question_type", default="synonyms",
                        help="Question type (e.g., synonyms, antonyms, analogies)")
    parser.add_argument("--difficulty", type=int, default=3, choices=[1,2,3,4,5])
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--host", default="http://localhost:1234/v1")
    parser.add_argument("--model", default="local-model")
    parser.add_argument("--list-types", action="store_true", help="List available question types")

    args = parser.parse_args()

    if args.list_types:
        print("\nVerbal Reasoning types:")
        for t in VR_TEMPLATES.keys():
            print(f"  - {t}")
        print("\nMathematics types:")
        for t in MATHS_TEMPLATES.keys():
            print(f"  - {t}")
        return

    print(f"""
╔══════════════════════════════════════════════════════╗
║           ExamTutor Question Generator               ║
╠══════════════════════════════════════════════════════╣
║  Subject: {args.subject:<40} ║
║  Type: {args.question_type:<43} ║
║  Difficulty: {args.difficulty}/5{' '*37}║
║  Count: {args.count:<44} ║
║  LLM: {args.host:<46} ║
╚══════════════════════════════════════════════════════╝
""")

    generator = QuestionGenerator(
        host=args.host,
        model=args.model,
    )

    questions = generator.generate(
        subject=args.subject,
        question_type=args.question_type,
        difficulty=args.difficulty,
        count=args.count,
    )

    if questions:
        output_dir = Path(__file__).parent.parent / "data" / "questions"
        save_questions(questions, output_dir)

        print("\n" + "="*50)
        print("Sample generated question:")
        print("="*50)
        q = questions[0]
        print(f"\n{q.question_text}\n")
        for i, opt in enumerate(q.options):
            marker = "→" if i == q.correct_index else " "
            print(f"  {marker} {chr(65+i)}) {opt}")
        print(f"\nExplanation: {q.explanation}")


if __name__ == "__main__":
    main()

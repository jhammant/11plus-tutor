#!/usr/bin/env python3
"""
Test the question generator with your local LLM
Run this to verify LLM connectivity before generating questions
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_llm_connection():
    """Test connection to local LLM"""
    print("Testing LLM connection...")
    print("=" * 50)

    try:
        from openai import OpenAI

        # Try LM Studio first (port 1234)
        hosts = [
            ("LM Studio", "http://localhost:1234/v1", "lm-studio"),
            ("Ollama", "http://localhost:11434/v1", "ollama"),
        ]

        for name, host, api_key in hosts:
            print(f"\nTrying {name} at {host}...")
            try:
                client = OpenAI(base_url=host, api_key=api_key)

                response = client.chat.completions.create(
                    model="local-model" if "1234" in host else "llama3.2",
                    messages=[
                        {"role": "user", "content": "Say 'Hello ExamTutor!' and nothing else."}
                    ],
                    max_tokens=20,
                    timeout=10,
                )

                result = response.choices[0].message.content
                print(f"  ✓ Connected! Response: {result}")
                return host, api_key

            except Exception as e:
                print(f"  ✗ Failed: {type(e).__name__}: {str(e)[:50]}")

        print("\n❌ No LLM server found!")
        print("\nPlease start one of:")
        print("  - LM Studio (loads model, start local server on port 1234)")
        print("  - Ollama (ollama run llama3.2)")
        return None, None

    except ImportError:
        print("❌ OpenAI package not installed. Run: pip install openai")
        return None, None


def test_question_generation(host, api_key):
    """Test generating a sample question"""
    print("\n" + "=" * 50)
    print("Testing question generation...")
    print("=" * 50)

    from scripts.generate_questions import QuestionGenerator

    model = "local-model" if "1234" in host else "llama3.2"
    generator = QuestionGenerator(host=host, api_key=api_key, model=model)

    print("\nGenerating a synonyms question...")
    questions = generator.generate(
        subject="verbal_reasoning",
        question_type="synonyms",
        difficulty=2,
        count=1,
    )

    if questions:
        q = questions[0]
        print("\n✓ Generated successfully!")
        print("\n" + "-" * 50)
        print(f"Question: {q.question_text}")
        print(f"\nOptions:")
        for i, opt in enumerate(q.options):
            marker = "→" if i == q.correct_index else " "
            print(f"  {marker} {chr(65+i)}) {opt}")
        print(f"\nAnswer: {q.correct_answer}")
        print(f"Explanation: {q.explanation}")
        return True
    else:
        print("❌ Failed to generate question")
        return False


def test_database():
    """Test database connection"""
    print("\n" + "=" * 50)
    print("Testing database...")
    print("=" * 50)

    try:
        from src.core.database import SessionLocal, Question

        db = SessionLocal()
        count = db.query(Question).count()
        print(f"  ✓ Database connected! Questions in bank: {count}")

        if count > 0:
            q = db.query(Question).first()
            print(f"  Sample: {q.question_type} - {q.question_text[:50]}...")

        db.close()
        return True

    except Exception as e:
        print(f"  ✗ Database error: {e}")
        return False


def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ExamTutor - System Test                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

    # Test database
    db_ok = test_database()

    # Test LLM
    host, api_key = test_llm_connection()

    if host:
        # Test generation
        gen_ok = test_question_generation(host, api_key)
    else:
        gen_ok = False

    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"  Database:     {'✓ OK' if db_ok else '✗ Failed'}")
    print(f"  LLM:          {'✓ OK' if host else '✗ Not connected'}")
    print(f"  Generation:   {'✓ OK' if gen_ok else '✗ Failed'}")

    if db_ok and host and gen_ok:
        print("\n🎉 All systems ready!")
        print("\nNext steps:")
        print("  1. Generate more questions:")
        print("     python scripts/generate_questions.py --subject verbal_reasoning --type synonyms --count 10")
        print("  2. Start the app:")
        print("     python scripts/start_app.py")
    elif db_ok and not host:
        print("\n⚠️  LLM not connected - start LM Studio or Ollama to generate questions")
        print("    The app will still work with the sample questions in the database.")


if __name__ == "__main__":
    main()

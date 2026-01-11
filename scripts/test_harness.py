#!/usr/bin/env python3
"""
Comprehensive Test Harness for 11+ Tutor
Tests all question types, API endpoints, and answer submission.

Usage:
    python scripts/test_harness.py
"""

import requests
import json
import sys
import sqlite3
from typing import Dict, List, Any, Optional

API_BASE = "http://localhost:8002"
DB_PATH = "elevenplustutor.db"

def get_correct_answer_from_db(question_id: str) -> Optional[Dict]:
    """Get correct answer directly from database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT correct_answer, correct_index, options FROM questions WHERE id = ?", (question_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return {
                "correct_answer": row["correct_answer"],
                "correct_index": row["correct_index"],
                "options": json.loads(row["options"]) if row["options"] else []
            }
    except Exception as e:
        print(f"DB error: {e}")
    return None

class TestResult:
    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.error = None
        self.details = {}

    def __repr__(self):
        status = "PASS" if self.passed else "FAIL"
        return f"[{status}] {self.name}"

def test_api_health() -> TestResult:
    """Test that API is running"""
    result = TestResult("API Health Check")
    try:
        resp = requests.get(f"{API_BASE}/", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "healthy":
                result.passed = True
                result.details = data
            else:
                result.error = f"API not healthy: {data}"
        else:
            result.error = f"HTTP {resp.status_code}"
    except Exception as e:
        result.error = str(e)
    return result

def test_get_questions(subject: str = None, question_type: str = None) -> TestResult:
    """Test fetching questions"""
    name = f"Get Questions ({subject or 'all'}/{question_type or 'all'})"
    result = TestResult(name)
    try:
        params = {"limit": 5}
        if subject:
            params["subject"] = subject
        if question_type:
            params["question_type"] = question_type

        resp = requests.get(f"{API_BASE}/api/questions", params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if len(data) > 0:
                result.passed = True
                result.details = {
                    "count": len(data),
                    "first_id": data[0]["id"],
                    "first_type": data[0]["question_type"]
                }
            else:
                result.error = "No questions returned"
        else:
            result.error = f"HTTP {resp.status_code}: {resp.text}"
    except Exception as e:
        result.error = str(e)
    return result

def test_submit_answer(question_id: str, answer: str, expected_correct: bool = None) -> TestResult:
    """Test submitting an answer"""
    result = TestResult(f"Submit Answer ({question_id[:8]}...)")
    try:
        payload = {
            "question_id": question_id,
            "student_id": "test-harness",
            "answer": answer,
            "time_taken_seconds": 10
        }
        resp = requests.post(f"{API_BASE}/api/submit", json=payload, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            result.passed = True
            result.details = {
                "is_correct": data.get("is_correct"),
                "correct_answer": data.get("correct_answer"),
                "feedback": data.get("feedback", "")[:50]
            }
            if expected_correct is not None and data.get("is_correct") != expected_correct:
                result.error = f"Expected correct={expected_correct}, got {data.get('is_correct')}"
                result.passed = False
        else:
            result.error = f"HTTP {resp.status_code}: {resp.text[:200]}"
    except Exception as e:
        result.error = str(e)
    return result

def test_question_type_flow(subject: str, question_type: str) -> List[TestResult]:
    """Test full flow for a question type: fetch, parse, submit"""
    results = []

    # Fetch question
    fetch_result = test_get_questions(subject, question_type)
    results.append(fetch_result)

    if not fetch_result.passed:
        return results

    # Get a question to test
    try:
        resp = requests.get(f"{API_BASE}/api/questions",
                          params={"subject": subject, "question_type": question_type, "limit": 1})
        questions = resp.json()
        if not questions:
            return results

        question = questions[0]

        # Get correct answer from database (API doesn't return it for security)
        db_data = get_correct_answer_from_db(question["id"])
        if db_data:
            question["correct_answer"] = db_data["correct_answer"]
            question["correct_index"] = db_data["correct_index"]

        # Test structure (correct_answer from DB, not API)
        struct_result = TestResult(f"Question Structure ({question_type})")
        required_fields = ["id", "question_text", "options"]
        missing = [f for f in required_fields if f not in question]
        if not missing and db_data:
            struct_result.passed = True
            struct_result.details = {
                "has_options": len(question.get("options", [])),
                "has_correct_answer": db_data is not None
            }
        else:
            struct_result.error = f"Missing fields: {missing}" if missing else "No DB data"
        results.append(struct_result)

        # Test SVG rendering for NVR
        if question_type.startswith("nvr_"):
            svg_result = TestResult(f"SVG Validity ({question_type})")
            try:
                qt = json.loads(question["question_text"])
                if "sequence" in qt:
                    svg = qt["sequence"][0]
                elif "shapes" in qt:
                    svg = qt["shapes"][0]
                elif "pair1" in qt:
                    svg = qt["pair1"][0]
                else:
                    svg = ""

                if svg.startswith("<svg") and svg.endswith("</svg>"):
                    svg_result.passed = True
                    svg_result.details = {"svg_length": len(svg)}
                else:
                    svg_result.error = "Invalid SVG format"
            except Exception as e:
                svg_result.error = str(e)
            results.append(svg_result)

        # Test comprehension structure
        if question_type == "comprehension":
            comp_result = TestResult("Comprehension Structure")
            try:
                qt = json.loads(question["question_text"])
                if all(k in qt for k in ["title", "passage", "question"]):
                    comp_result.passed = True
                    comp_result.details = {
                        "title": qt["title"],
                        "passage_length": len(qt["passage"])
                    }
                else:
                    comp_result.error = "Missing comprehension fields"
            except Exception as e:
                comp_result.error = str(e)
            results.append(comp_result)

        # Test answer submission with correct answer
        correct_answer = question.get("correct_answer", "")
        correct_index = question.get("correct_index")
        options = question.get("options", [])

        # Determine what to submit as the answer
        # For most questions, submit the option at correct_index (what the frontend does)
        if correct_index is not None and correct_index < len(options):
            actual_answer = options[correct_index]
        else:
            actual_answer = correct_answer

        submit_result = test_submit_answer(question["id"], actual_answer, expected_correct=True)
        results.append(submit_result)

        # Test wrong answer
        wrong_answer = "DEFINITELY_WRONG_ANSWER_12345"
        wrong_result = test_submit_answer(question["id"], wrong_answer, expected_correct=False)
        wrong_result.name = f"Wrong Answer Test ({question_type})"
        results.append(wrong_result)

    except Exception as e:
        error_result = TestResult(f"Flow Error ({question_type})")
        error_result.error = str(e)
        results.append(error_result)

    return results

def run_all_tests() -> Dict[str, Any]:
    """Run all tests and return summary"""
    all_results = []

    print("=" * 60)
    print("11+ TUTOR TEST HARNESS")
    print("=" * 60)

    # Test API health
    print("\n[1] Testing API Health...")
    health = test_api_health()
    all_results.append(health)
    print(f"    {health}")

    if not health.passed:
        print("\n    ERROR: API not running! Start with:")
        print("    cd /Users/jhammant/dev/ExamTutor && source venv/bin/activate")
        print("    uvicorn src.api.main:app --port 8002")
        return {"passed": 0, "failed": 1, "results": all_results}

    # Test each question type
    question_types = [
        ("verbal_reasoning", "synonyms"),
        ("verbal_reasoning", "antonyms"),
        ("verbal_reasoning", "letter_sequences"),
        ("verbal_reasoning", "hidden_words"),
        ("verbal_reasoning", "compound_words"),
        ("mathematics", "sequences"),
        ("mathematics", "arithmetic"),
        ("non_verbal_reasoning", "nvr_sequences"),
        ("non_verbal_reasoning", "nvr_odd_one_out"),
        ("non_verbal_reasoning", "nvr_analogies"),
        ("english", "comprehension"),
        ("english", "spelling"),
        ("english", "grammar"),
    ]

    print(f"\n[2] Testing {len(question_types)} Question Types...")
    for i, (subject, qtype) in enumerate(question_types, 1):
        print(f"\n    [{i}/{len(question_types)}] {subject}/{qtype}")
        results = test_question_type_flow(subject, qtype)
        all_results.extend(results)
        for r in results:
            status = "PASS" if r.passed else "FAIL"
            print(f"        [{status}] {r.name}")
            if r.error:
                print(f"             Error: {r.error}")

    # Summary
    passed = sum(1 for r in all_results if r.passed)
    failed = sum(1 for r in all_results if not r.passed)

    print("\n" + "=" * 60)
    print(f"SUMMARY: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed > 0:
        print("\nFailed tests:")
        for r in all_results:
            if not r.passed:
                print(f"  - {r.name}: {r.error}")

    return {
        "passed": passed,
        "failed": failed,
        "results": all_results
    }

if __name__ == "__main__":
    summary = run_all_tests()
    sys.exit(0 if summary["failed"] == 0 else 1)

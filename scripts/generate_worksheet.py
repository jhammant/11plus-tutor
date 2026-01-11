#!/usr/bin/env python3
"""
Generate Printable Worksheets for 11+ Practice

Creates PDF-ready HTML worksheets that parents can print for offline practice.

Usage:
    python scripts/generate_worksheet.py --subject mathematics --count 20
    python scripts/generate_worksheet.py --type synonyms --count 15
    python scripts/generate_worksheet.py --mixed --count 25
"""

import sqlite3
import json
import argparse
import random
from datetime import datetime
from pathlib import Path

def get_questions(db_path: str, subject: str = None, question_type: str = None,
                  count: int = 20, exclude_nvr: bool = True) -> list:
    """Fetch questions from database"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    query = "SELECT * FROM questions WHERE 1=1"
    params = []

    if subject:
        query += " AND subject = ?"
        params.append(subject)

    if question_type:
        query += " AND question_type = ?"
        params.append(question_type)

    # Exclude NVR by default (SVG doesn't print well without special handling)
    if exclude_nvr:
        query += " AND subject != 'non_verbal_reasoning'"

    # Also exclude comprehension (passages too long for worksheets)
    query += " AND question_type != 'comprehension'"

    query += " ORDER BY RANDOM() LIMIT ?"
    params.append(count)

    cur.execute(query, params)
    questions = [dict(row) for row in cur.fetchall()]
    conn.close()

    return questions

def generate_html_worksheet(questions: list, title: str = "11+ Practice Worksheet") -> str:
    """Generate printable HTML worksheet"""

    date_str = datetime.now().strftime("%d %B %Y")

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        @media print {{
            body {{ margin: 0; }}
            .no-print {{ display: none; }}
            .page-break {{ page-break-after: always; }}
        }}

        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.4;
        }}

        .header {{
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #333;
            padding-bottom: 15px;
        }}

        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}

        .header p {{
            margin: 5px 0;
            color: #666;
        }}

        .student-info {{
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }}

        .student-info label {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .student-info input {{
            border: none;
            border-bottom: 1px solid #333;
            width: 150px;
            padding: 5px;
        }}

        .question {{
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 1px solid #eee;
        }}

        .question-number {{
            font-weight: bold;
            color: #333;
        }}

        .question-text {{
            margin: 10px 0;
            font-size: 14px;
        }}

        .options {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
            margin-top: 10px;
        }}

        .option {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .option-circle {{
            width: 18px;
            height: 18px;
            border: 2px solid #333;
            border-radius: 50%;
            flex-shrink: 0;
        }}

        .answer-section {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #333;
        }}

        .answer-section h2 {{
            font-size: 16px;
            margin-bottom: 15px;
        }}

        .answers {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 10px;
            font-size: 12px;
        }}

        .answer-item {{
            padding: 5px;
            background: #f5f5f5;
            border-radius: 4px;
        }}

        .instructions {{
            background: #f9f9f9;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 13px;
        }}

        .score-box {{
            float: right;
            border: 2px solid #333;
            padding: 15px;
            text-align: center;
            min-width: 80px;
        }}

        .score-box .score {{
            font-size: 24px;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <p>Date: {date_str} | Questions: {len(questions)}</p>
    </div>

    <div class="student-info no-print">
        <label>Name: <input type="text" placeholder=""></label>
        <label>Time: <input type="text" placeholder="__ minutes"></label>
        <div class="score-box">
            <div class="score">__/{len(questions)}</div>
            <div>Score</div>
        </div>
    </div>

    <div class="instructions">
        <strong>Instructions:</strong> Read each question carefully. Fill in the circle next to your chosen answer.
        Work through all questions before checking your answers. Time yourself if practicing for the exam.
    </div>

    <div class="questions">
"""

    for i, q in enumerate(questions, 1):
        options = json.loads(q['options']) if isinstance(q['options'], str) else q['options']

        # Clean up question text (remove JSON for special types)
        question_text = q['question_text']
        if question_text.startswith('{'):
            try:
                parsed = json.loads(question_text)
                question_text = parsed.get('question', parsed.get('instruction', question_text))
            except:
                pass

        html += f"""
        <div class="question">
            <span class="question-number">Q{i}.</span>
            <span class="question-type" style="color: #888; font-size: 11px;">({q['question_type'].replace('_', ' ').title()})</span>
            <div class="question-text">{question_text}</div>
            <div class="options">
"""

        for j, opt in enumerate(options):
            letter = chr(65 + j)
            # Truncate long options (like SVG)
            display_opt = opt[:100] + "..." if len(str(opt)) > 100 else opt
            html += f"""
                <div class="option">
                    <div class="option-circle"></div>
                    <span><strong>{letter}.</strong> {display_opt}</span>
                </div>
"""

        html += """
            </div>
        </div>
"""

    # Answer key (for parents)
    html += """
    <div class="page-break"></div>
    <div class="answer-section">
        <h2>Answer Key (for parents - tear off before giving to child)</h2>
        <div class="answers">
"""

    for i, q in enumerate(questions, 1):
        options = json.loads(q['options']) if isinstance(q['options'], str) else q['options']
        correct_idx = q['correct_index'] if q['correct_index'] is not None else 0
        correct_letter = chr(65 + correct_idx)

        html += f"""
            <div class="answer-item">
                <strong>Q{i}:</strong> {correct_letter}
            </div>
"""

    html += """
        </div>
    </div>
</body>
</html>
"""

    return html

def main():
    parser = argparse.ArgumentParser(description='Generate printable 11+ worksheets')
    parser.add_argument('--subject', choices=['verbal_reasoning', 'mathematics', 'english'])
    parser.add_argument('--type', help='Specific question type (e.g., synonyms, sequences)')
    parser.add_argument('--count', type=int, default=20, help='Number of questions')
    parser.add_argument('--mixed', action='store_true', help='Mix all question types')
    parser.add_argument('--output', default='worksheet.html', help='Output filename')
    parser.add_argument('--db', default='elevenplustutor.db', help='Database path')
    args = parser.parse_args()

    # Get questions
    questions = get_questions(
        args.db,
        subject=args.subject if not args.mixed else None,
        question_type=args.type,
        count=args.count
    )

    if not questions:
        print("No questions found matching criteria")
        return

    # Generate title
    if args.type:
        title = f"11+ Practice: {args.type.replace('_', ' ').title()}"
    elif args.subject:
        title = f"11+ Practice: {args.subject.replace('_', ' ').title()}"
    else:
        title = "11+ Mixed Practice Worksheet"

    # Generate HTML
    html = generate_html_worksheet(questions, title)

    # Save
    output_path = Path(args.output)
    output_path.write_text(html)

    print(f"Worksheet generated: {output_path}")
    print(f"  - {len(questions)} questions")
    print(f"  - Open in browser and print (Ctrl+P / Cmd+P)")
    print(f"  - Answer key included on last page")

if __name__ == '__main__':
    main()

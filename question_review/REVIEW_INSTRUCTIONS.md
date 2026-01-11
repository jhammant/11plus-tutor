# Question Review Instructions

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

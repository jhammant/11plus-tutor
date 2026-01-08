"""
Practice Agent
Generates practice questions and evaluates student answers
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from src.question_bank.models import (
    Question,
    ExamType,
    Subject,
    Difficulty,
    QuestionFormat,
    VR_QUESTION_TYPES,
    NVR_QUESTION_TYPES,
)


@dataclass
class GenerationRequest:
    """Request to generate a question"""
    exam_type: ExamType
    subject: Subject
    topic: Optional[str] = None
    question_type: Optional[str] = None
    difficulty: Difficulty = Difficulty.MEDIUM


@dataclass
class EvaluationResult:
    """Result of evaluating a student's answer"""
    is_correct: bool
    marks_awarded: int
    marks_available: int
    feedback: str
    model_answer: str
    explanation: Optional[str] = None


class PracticeAgent:
    """Agent for generating and evaluating practice questions"""

    def __init__(self, llm_client: Any):
        """
        Initialize the practice agent

        Args:
            llm_client: Client for LLM API (OpenAI, Ollama, etc.)
        """
        self.llm = llm_client

    async def generate_question(self, request: GenerationRequest) -> Question:
        """
        Generate a practice question

        Args:
            request: Specification for the question to generate

        Returns:
            A new Question object
        """
        # Build the generation prompt based on exam type and subject
        prompt = self._build_generation_prompt(request)

        # Call LLM to generate question
        response = await self.llm.generate(prompt)

        # Parse response into Question object
        question = self._parse_generated_question(response, request)

        return question

    def _build_generation_prompt(self, request: GenerationRequest) -> str:
        """Build prompt for question generation"""

        if request.subject == Subject.VERBAL_REASONING:
            return self._build_vr_prompt(request)
        elif request.subject == Subject.NON_VERBAL_REASONING:
            return self._build_nvr_prompt(request)
        elif request.subject == Subject.MATHEMATICS:
            return self._build_maths_prompt(request)
        elif request.subject == Subject.ENGLISH:
            return self._build_english_prompt(request)
        else:
            return self._build_generic_prompt(request)

    def _build_vr_prompt(self, request: GenerationRequest) -> str:
        """Build prompt for Verbal Reasoning questions"""
        question_type = request.question_type or "synonyms"
        difficulty_desc = {
            Difficulty.FOUNDATION: "very easy, using common words",
            Difficulty.EASY: "easy, using familiar words",
            Difficulty.MEDIUM: "moderate, using curriculum-appropriate vocabulary",
            Difficulty.HARD: "challenging, using advanced vocabulary",
            Difficulty.CHALLENGE: "very challenging, requiring strong vocabulary"
        }

        examples = {
            "synonyms": """
Example: Find two words, one from each group, that are closest in meaning.
(happy, sad, angry) (joyful, upset, calm)
Answer: happy, joyful""",
            "antonyms": """
Example: Find two words, one from each group, that are most opposite in meaning.
(hot, warm, cold) (freezing, boiling, tepid)
Answer: hot, freezing""",
            "code_words": """
Example: If the code for CAMP is ECOR, what is the code for DAMP?
Answer: FCOR (each letter is shifted by 2)""",
            "analogies": """
Example: Bird is to nest as bee is to ____
Answer: hive""",
        }

        return f"""Generate a {question_type} question for the 11+ Verbal Reasoning exam.

Difficulty: {difficulty_desc.get(request.difficulty, 'moderate')}
Target age: 10-11 years old
Format: Multiple choice with 5 options

{examples.get(question_type, '')}

Generate a new question following this exact format:
1. Question text
2. Five answer options (A-E)
3. Correct answer with letter
4. Brief explanation of why this is correct

Ensure the question is:
- Age-appropriate
- Clear and unambiguous
- Has exactly one correct answer
- Tests the {question_type} skill effectively"""

    def _build_nvr_prompt(self, request: GenerationRequest) -> str:
        """Build prompt for Non-Verbal Reasoning questions"""
        # NVR is harder to generate with text - would need image generation
        # For now, describe the question pattern
        question_type = request.question_type or "sequences"

        return f"""Describe a Non-Verbal Reasoning {question_type} question for the 11+ exam.

Note: This will need to be converted to images for actual use.

Describe:
1. The pattern/sequence (describe shapes, transformations)
2. What changes between each step
3. What the answer should be
4. Why this tests {question_type} skills

Target difficulty: {request.difficulty.name}
Target age: 10-11 years old"""

    def _build_maths_prompt(self, request: GenerationRequest) -> str:
        """Build prompt for Mathematics questions"""
        topic = request.topic or "general"
        exam_type = request.exam_type

        if exam_type == ExamType.ELEVEN_PLUS_GL:
            context = "11+ Grammar School Entrance Exam (GL Assessment format)"
            curriculum = "KS2 National Curriculum"
        else:
            context = "GCSE Mathematics"
            curriculum = "KS4 National Curriculum"

        return f"""Generate a mathematics question for {context}.

Topic: {topic}
Difficulty: {request.difficulty.name}
Curriculum: {curriculum}

Requirements:
1. Age-appropriate language
2. Clear, unambiguous question
3. Numerical answer or multiple choice
4. Include working/method marks if applicable

Generate:
1. Question text (including any necessary context)
2. Answer options (if multiple choice) OR space for working
3. Correct answer
4. Mark scheme (how marks are awarded)
5. Worked solution"""

    def _build_english_prompt(self, request: GenerationRequest) -> str:
        """Build prompt for English questions"""
        topic = request.topic or "comprehension"

        return f"""Generate an English {topic} question for the 11+ exam.

Type: {topic}
Difficulty: {request.difficulty.name}
Target age: 10-11 years old

For comprehension: Include a short passage (100-150 words) followed by questions.
For grammar/spelling: Provide clear context and options.
For vocabulary: Use age-appropriate but challenging words.

Generate:
1. Passage or context (if needed)
2. Question text
3. Answer options (if multiple choice)
4. Correct answer
5. Explanation"""

    def _build_generic_prompt(self, request: GenerationRequest) -> str:
        """Build generic prompt for other subjects"""
        return f"""Generate a {request.subject.value} question.

Exam type: {request.exam_type.value}
Topic: {request.topic or 'general'}
Difficulty: {request.difficulty.name}

Generate a well-structured question with:
1. Clear question text
2. Answer options (if applicable)
3. Correct answer
4. Mark scheme
5. Explanation"""

    def _parse_generated_question(
        self,
        response: str,
        request: GenerationRequest
    ) -> Question:
        """Parse LLM response into a Question object"""
        # This would parse the LLM's structured response
        # For now, return a placeholder
        import uuid

        return Question(
            id=str(uuid.uuid4()),
            exam_type=request.exam_type,
            subject=request.subject,
            topic=request.topic or "general",
            subtopic=None,
            question_type=request.question_type or "general",
            difficulty=request.difficulty,
            format=QuestionFormat.MULTIPLE_CHOICE,
            question_text=response,  # Would be parsed properly
            correct_answer="",  # Would be extracted
            source="generated",
        )

    async def evaluate_answer(
        self,
        question: Question,
        student_answer: str
    ) -> EvaluationResult:
        """
        Evaluate a student's answer

        Args:
            question: The question that was answered
            student_answer: The student's response

        Returns:
            EvaluationResult with feedback
        """
        # For simple questions, direct comparison
        if question.format == QuestionFormat.MULTIPLE_CHOICE:
            is_correct = student_answer.strip().upper() == question.correct_answer.strip().upper()
            marks = question.marks_available if is_correct else 0

            return EvaluationResult(
                is_correct=is_correct,
                marks_awarded=marks,
                marks_available=question.marks_available,
                feedback="Correct!" if is_correct else f"The correct answer was {question.correct_answer}",
                model_answer=question.correct_answer,
                explanation=question.worked_solution,
            )

        # For longer answers, use LLM to evaluate
        prompt = f"""Evaluate this student's answer against the mark scheme.

Question: {question.question_text}

Mark Scheme: {question.mark_scheme or question.correct_answer}

Student Answer: {student_answer}

Marks Available: {question.marks_available}

Provide:
1. Marks awarded (0-{question.marks_available})
2. What was correct
3. What was missing or incorrect
4. Model answer for comparison"""

        response = await self.llm.generate(prompt)

        # Parse response (simplified)
        return EvaluationResult(
            is_correct=False,  # Would be parsed
            marks_awarded=0,  # Would be parsed
            marks_available=question.marks_available,
            feedback=response,
            model_answer=question.correct_answer,
            explanation=question.worked_solution,
        )

    async def explain_concept(
        self,
        topic: str,
        subject: Subject,
        age_group: str = "10-11"
    ) -> str:
        """
        Explain a concept at an age-appropriate level

        Args:
            topic: The concept to explain
            subject: The subject area
            age_group: Target age range

        Returns:
            Clear explanation of the concept
        """
        prompt = f"""Explain the concept of "{topic}" in {subject.value} for a student aged {age_group}.

Requirements:
- Use simple, clear language
- Include an example
- Relate to things they might know
- Keep it concise (2-3 paragraphs)
- If relevant, mention how this might appear in exams"""

        return await self.llm.generate(prompt)

    async def generate_hint(
        self,
        question: Question,
        previous_attempt: Optional[str] = None
    ) -> str:
        """
        Generate a helpful hint for a question

        Args:
            question: The question to provide a hint for
            previous_attempt: The student's previous wrong answer (if any)

        Returns:
            A helpful hint without giving away the answer
        """
        prompt = f"""Provide a helpful hint for this question without giving away the answer.

Question: {question.question_text}
Question Type: {question.question_type}

{"Previous wrong answer: " + previous_attempt if previous_attempt else ""}

Provide a hint that:
- Points them in the right direction
- Doesn't reveal the answer
- Uses encouraging language
- Is specific to this question type"""

        return await self.llm.generate(prompt)

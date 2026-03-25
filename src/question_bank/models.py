"""
Question Bank Data Models
Core data structures for questions, answers, and evaluations
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any


class ExamType(Enum):
    """Supported exam types"""
    ELEVEN_PLUS_GL = "11plus_gl"
    ELEVEN_PLUS_CEM = "11plus_cem"
    GCSE_AQA = "gcse_aqa"
    GCSE_EDEXCEL = "gcse_edexcel"
    GCSE_OCR = "gcse_ocr"


class Subject(Enum):
    """Subject areas"""
    # 11+ subjects
    VERBAL_REASONING = "verbal_reasoning"
    NON_VERBAL_REASONING = "non_verbal_reasoning"

    # Core subjects
    MATHEMATICS = "mathematics"
    ENGLISH = "english"

    # GCSE Sciences
    BIOLOGY = "biology"
    CHEMISTRY = "chemistry"
    PHYSICS = "physics"
    COMBINED_SCIENCE = "combined_science"

    # GCSE Options
    HISTORY = "history"
    GEOGRAPHY = "geography"
    COMPUTER_SCIENCE = "computer_science"
    FRENCH = "french"
    SPANISH = "spanish"
    GERMAN = "german"


class Difficulty(Enum):
    """Question difficulty levels"""
    FOUNDATION = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4
    CHALLENGE = 5


class QuestionFormat(Enum):
    """Question presentation formats"""
    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"
    LONG_ANSWER = "long_answer"
    FILL_BLANK = "fill_blank"
    MATCHING = "matching"
    ORDERING = "ordering"
    TRUE_FALSE = "true_false"
    DIAGRAM = "diagram"


@dataclass
class Question:
    """A single question in the question bank"""
    id: str
    exam_type: ExamType
    subject: Subject
    topic: str
    subtopic: Optional[str]
    question_type: str  # e.g., "synonyms", "sequences", "algebra"
    difficulty: Difficulty
    format: QuestionFormat

    # Question content
    question_text: str
    question_image: Optional[str] = None  # Path or URL to image
    context: Optional[str] = None  # Additional context (e.g., passage for comprehension)

    # Answer options (for multiple choice)
    options: Optional[List[str]] = None

    # Correct answer
    correct_answer: str
    correct_answer_index: Optional[int] = None  # For multiple choice

    # Mark scheme
    marks_available: int = 1
    mark_scheme: Optional[str] = None  # Detailed marking criteria

    # Explanation
    worked_solution: Optional[str] = None
    hint: Optional[str] = None

    # Metadata
    source: str = "generated"  # generated, oak_api, past_paper
    source_reference: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    # Statistics
    times_attempted: int = 0
    times_correct: int = 0

    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        if self.times_attempted == 0:
            return 0.0
        return self.times_correct / self.times_attempted


@dataclass
class AttemptRecord:
    """Record of a student's attempt at a question"""
    id: str
    student_id: str
    question_id: str
    timestamp: datetime

    # Response
    student_answer: str
    time_taken_seconds: int

    # Evaluation
    is_correct: bool
    marks_awarded: int
    marks_available: int

    # Feedback
    feedback: Optional[str] = None
    model_answer_shown: bool = False


@dataclass
class StudentProgress:
    """Track a student's learning progress"""
    student_id: str
    exam_target: ExamType
    target_date: Optional[datetime] = None

    # Topic mastery (topic -> score 0-1)
    topic_mastery: Dict[str, float] = field(default_factory=dict)

    # Weak areas identified
    weak_topics: List[str] = field(default_factory=list)

    # Practice history
    total_questions_attempted: int = 0
    total_correct: int = 0

    # Predicted performance
    predicted_score: Optional[float] = None
    predicted_grade: Optional[str] = None

    # Learning streak
    current_streak_days: int = 0
    longest_streak_days: int = 0
    last_practice_date: Optional[datetime] = None


@dataclass
class MockExam:
    """A mock exam paper"""
    id: str
    exam_type: ExamType
    subject: Subject
    paper_name: str

    # Configuration
    time_limit_minutes: int
    questions: List[Question]
    total_marks: int

    # Instructions
    instructions: str = ""
    calculator_allowed: bool = True


@dataclass
class MockExamResult:
    """Result of a completed mock exam"""
    id: str
    student_id: str
    mock_exam_id: str
    timestamp: datetime

    # Performance
    time_taken_minutes: int
    marks_achieved: int
    marks_available: int
    percentage: float

    # Question-by-question results
    question_results: List[AttemptRecord]

    # Analysis
    strong_topics: List[str] = field(default_factory=list)
    weak_topics: List[str] = field(default_factory=list)
    examiner_feedback: Optional[str] = None

    @property
    def grade(self) -> str:
        """Calculate grade based on percentage"""
        if self.percentage >= 90:
            return "9"
        elif self.percentage >= 80:
            return "8"
        elif self.percentage >= 70:
            return "7"
        elif self.percentage >= 60:
            return "6"
        elif self.percentage >= 50:
            return "5"
        elif self.percentage >= 40:
            return "4"
        elif self.percentage >= 30:
            return "3"
        elif self.percentage >= 20:
            return "2"
        else:
            return "1"


# Verbal Reasoning specific question types
VR_QUESTION_TYPES = [
    "synonyms",
    "antonyms",
    "analogies",
    "odd_one_out",
    "code_words",
    "letter_sequences",
    "hidden_words",
    "compound_words",
    "cloze_passages",
    "shuffled_sentences",
    "word_connections",
    "letter_codes",
    "number_codes",
    "word_matrices",
    "logical_deduction",
    "alphabet_position",
    "word_ladders",
    "anagrams",
    "word_pairs",
    "missing_letters",
    "double_meanings",
]

# Non-Verbal Reasoning specific question types
NVR_QUESTION_TYPES = [
    "sequences",
    "matrices",
    "analogies",
    "odd_one_out",
    "rotations",
    "reflections",
    "transformations",
    "paper_folding",
    "nets_and_cubes",
    "embedded_shapes",
    "code_breakers",
    "spatial_reasoning",
]


# New dataclasses for teaching strategies and adaptive difficulty

@dataclass
class TeachingStrategy:
    """Teaching strategy for a specific question type"""
    question_type: str
    subject: str  # e.g., "verbal_reasoning"
    title: str
    what_is_it: str  # Explanation of the question type
    approach: List[str]  # Step-by-step approach
    common_mistakes: List[str]
    time_tips: List[str]
    worked_examples: List["WorkedExample"]
    typical_time_seconds: int
    difficulty_range: str  # e.g., "Easy to Medium"
    is_free: bool = True


@dataclass
class WorkedExample:
    """A worked example for a question type"""
    question: str
    answer: str
    walkthrough: Optional[str] = None
    options: Optional[List[str]] = None


@dataclass
class AdaptiveDifficultyConfig:
    """Configuration for adaptive difficulty adjustment"""
    initial_difficulty: Difficulty = Difficulty.MEDIUM
    min_difficulty: Difficulty = Difficulty.FOUNDATION
    max_difficulty: Difficulty = Difficulty.CHALLENGE
    correct_streak_threshold: int = 3  # Increase difficulty after this many correct answers in a row
    incorrect_streak_threshold: int = 2  # Decrease difficulty after this many incorrect answers in a row
    difficulty_step: float = 0.5  # How much to adjust difficulty per streak


@dataclass
class QuestionBank:
    """A collection of questions with metadata"""
    questions: List[Question] = field(default_factory=list)
    strategies: Dict[str, TeachingStrategy] = field(default_factory=dict)  # question_type -> strategy
    difficulty_config: AdaptiveDifficultyConfig = field(default_factory=AdaptiveDifficultyConfig)

    def get_question_by_id(self, question_id: str) -> Optional[Question]:
        """Retrieve a question by its ID"""
        for q in self.questions:
            if q.id == question_id:
                return q
        return None

    def get_questions_by_subject(self, subject: Subject) -> List[Question]:
        """Get all questions for a specific subject"""
        return [q for q in self.questions if q.subject == subject]

    def get_questions_by_type(self, question_type: str) -> List[Question]:
        """Get all questions of a specific type"""
        return [q for q in self.questions if q.question_type == question_type]

    def get_next_question(self, student_progress: StudentProgress) -> Optional[Question]:
        """Get the next question based on adaptive difficulty and progress"""
        # Start with questions the student hasn't attempted
        unattempted = [q for q in self.questions if not any(
            ar.question_id == q.id for ar in student_progress.total_questions_attempted
        )]

        if not unattempted:
            # If all questions attempted, use any question
            unattempted = self.questions

        # Filter by difficulty based on student's performance
        current_difficulty = self._calculate_current_difficulty(student_progress)
        filtered_questions = [
            q for q in unattempted
            if abs(q.difficulty.value - current_difficulty) <= 1
        ]

        # If no questions in the desired difficulty range, fall back to any question
        if not filtered_questions:
            filtered_questions = unattempted

        # Return a random question from the filtered list
        import random
        return random.choice(filtered_questions) if filtered_questions else None

    def _calculate_current_difficulty(self, student_progress: StudentProgress) -> int:
        """Calculate the current difficulty level based on student performance"""
        config = self.difficulty_config
        correct_streak = 0
        incorrect_streak = 0

        # Calculate streaks from recent attempts (simplified for now)
        # In a real implementation, you'd analyze the student's recent attempts
        if student_progress.total_questions_attempted > 0:
            accuracy = student_progress.total_correct / student_progress.total_questions_attempted
            if accuracy >= 0.8:
                correct_streak = config.correct_streak_threshold
            elif accuracy <= 0.4:
                incorrect_streak = config.incorrect_streak_threshold

        # Calculate difficulty based on streaks
        base_difficulty = config.initial_difficulty.value
        if correct_streak >= config.correct_streak_threshold:
            base_difficulty += 1
        elif incorrect_streak >= config.incorrect_streak_threshold:
            base_difficulty -= 1

        # Clamp difficulty within bounds
        return max(config.min_difficulty.value, min(config.max_difficulty.value, base_difficulty))

"use client";

import { useState, useEffect, useCallback, Suspense, useMemo } from "react";
import { useSearchParams } from "next/navigation";
import {
  Clock,
  CheckCircle2,
  XCircle,
  ChevronRight,
  RotateCcw,
  Timer,
  Zap,
  Target,
} from "lucide-react";

// Component to safely render SVG content
function SVGRenderer({ svg, className = "" }: { svg: string; className?: string }) {
  return (
    <div
      className={className}
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  );
}

// Parse special question formats (NVR, comprehension)
interface ParsedQuestion {
  type: "text" | "nvr_sequence" | "nvr_odd_one_out" | "nvr_analogy" | "comprehension";
  instruction?: string;
  sequence?: string[];
  shapes?: string[];
  pair1?: string[];
  pair2_first?: string;
  passage?: string;
  title?: string;
  question?: string;
  rawText?: string;
}

function parseQuestionText(text: string, questionType: string): ParsedQuestion {
  try {
    const parsed = JSON.parse(text);
    if (parsed.type === "nvr_sequence") {
      return { type: "nvr_sequence", instruction: parsed.instruction, sequence: parsed.sequence };
    }
    if (parsed.type === "nvr_odd_one_out") {
      return { type: "nvr_odd_one_out", instruction: parsed.instruction, shapes: parsed.shapes };
    }
    if (parsed.type === "nvr_analogy") {
      return { type: "nvr_analogy", instruction: parsed.instruction, pair1: parsed.pair1, pair2_first: parsed.pair2_first };
    }
    if (parsed.type === "comprehension") {
      return { type: "comprehension", title: parsed.title, passage: parsed.passage, question: parsed.question };
    }
  } catch {
    // Not JSON, treat as plain text
  }
  return { type: "text", rawText: text };
}

// Check if an option is SVG
function isSVG(str: string): boolean {
  return str.trim().startsWith("<svg");
}

// Alphabet helper component for code words
function AlphabetHelper() {
  const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
  return (
    <div className="bg-slate-100 dark:bg-slate-700/50 rounded-lg p-3 mb-4">
      <div className="text-xs text-slate-500 dark:text-slate-400 mb-2 font-medium">Alphabet Reference:</div>
      <div className="flex flex-wrap gap-1 justify-center">
        {letters.map((letter, i) => (
          <div key={letter} className="flex flex-col items-center">
            <span className="text-sm font-bold text-slate-700 dark:text-slate-200">{letter}</span>
            <span className="text-xs text-slate-400 dark:text-slate-500">{i + 1}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// Strategy tips for each question type
function getStrategyTip(questionType: string): string {
  const tips: Record<string, string> = {
    synonyms: "Look for words that mean the SAME thing. Try replacing one word with another in a sentence.",
    antonyms: "Look for words that mean the OPPOSITE. Hot/cold, big/small, happy/sad.",
    analogies: "Find the relationship in the first pair, then apply it to find the answer.",
    odd_one_out: "Find what 4 words have in common - the odd one out doesn't fit that pattern.",
    code_words: "Use the alphabet reference! Work out how many positions each letter shifts.",
    letter_sequences: "Look for patterns: +1, +2, skip letters, or reverse order.",
    hidden_words: "The hidden word spans across TWO words. Look at the end of one and start of next.",
    compound_words: "Find two words that join together to make a new word (sun + flower = sunflower).",
    arithmetic: "Read carefully! Check if it's add, subtract, multiply, or divide. Show your working.",
    fractions: "Find common denominators for adding/subtracting. For multiplying, multiply tops and bottoms.",
    sequences: "Look at the gaps between numbers. Is it adding, multiplying, or something else?",
    nvr_sequences: "Watch for rotation, reflection, size changes, and colour patterns.",
    nvr_odd_one_out: "Look at shapes, shading, rotation, and number of sides. One is different!",
    nvr_analogies: "What happened to change shape 1 into shape 2? Apply the same change to shape 3.",
    comprehension: "Read the passage carefully first. Look for key words in the question.",
    spelling: "Sound out the word. Think about common spelling patterns and exceptions.",
    grammar: "Read the sentence aloud in your head. Does it sound right?",
  };
  return tips[questionType] || "Read the question carefully and think before choosing your answer.";
}

// Strategy tip component
function StrategyTip({ questionType, show, onToggle }: { questionType: string; show: boolean; onToggle: () => void }) {
  const tip = getStrategyTip(questionType);
  return (
    <div className="mb-4">
      <button
        onClick={onToggle}
        className="text-sm text-amber-600 hover:text-amber-700 dark:text-amber-400 dark:hover:text-amber-300 flex items-center gap-1 transition-colors"
      >
        <span className="text-base">💡</span>
        <span>{show ? "Hide" : "Show"} Strategy Tip</span>
        <kbd className="ml-2 px-1.5 py-0.5 bg-slate-200 dark:bg-slate-700 rounded text-xs font-mono">H</kbd>
      </button>
      {show && (
        <div className="mt-2 p-3 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg text-sm text-amber-800 dark:text-amber-200">
          <strong>Strategy:</strong> {tip}
        </div>
      )}
    </div>
  );
}

interface Question {
  id: string;
  exam_type: string;
  subject: string;
  topic: string;
  question_type: string;
  difficulty: number;
  question_text: string;
  options: string[];
  marks_available: number;
}

interface AnswerResult {
  is_correct: boolean;
  marks_awarded: number;
  marks_available: number;
  correct_answer: string;
  feedback: string;
  worked_solution: string | null;
}

const API_BASE = "http://localhost:8002";

function PracticeContent() {
  const searchParams = useSearchParams();
  const urlSubject = searchParams.get("subject") || "";
  const urlType = searchParams.get("type") || "";

  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [result, setResult] = useState<AnswerResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [score, setScore] = useState({ correct: 0, total: 0 });
  const [filter, setFilter] = useState({ subject: urlSubject, questionType: urlType });

  // Timer state
  const [timerEnabled, setTimerEnabled] = useState(false);
  const [timeRemaining, setTimeRemaining] = useState(45 * 60); // 45 mins in seconds
  const [questionStartTime, setQuestionStartTime] = useState<number>(Date.now());

  // Hint state
  const [showHint, setShowHint] = useState(false);

  // Streak tracking
  const [currentStreak, setCurrentStreak] = useState(0);
  const [showCelebration, setShowCelebration] = useState(false);

  // Per-question timer (counts up)
  const [questionTime, setQuestionTime] = useState(0);
  const [lastAnswerTime, setLastAnswerTime] = useState<number | null>(null);

  // Recommended time per question (50 seconds typical for 11+)
  const RECOMMENDED_TIME = 50;

  // Timer effect (overall exam timer)
  useEffect(() => {
    if (!timerEnabled || timeRemaining <= 0) return;

    const interval = setInterval(() => {
      setTimeRemaining((t) => Math.max(0, t - 1));
    }, 1000);

    return () => clearInterval(interval);
  }, [timerEnabled, timeRemaining]);

  // Per-question timer effect
  useEffect(() => {
    if (result) return; // Stop when answered

    const interval = setInterval(() => {
      setQuestionTime((t) => t + 1);
    }, 1000);

    return () => clearInterval(interval);
  }, [result, currentQuestion]);

  // Get timer color based on time spent
  const getTimerColor = (seconds: number) => {
    if (seconds < 30) return "text-green-600 dark:text-green-400";
    if (seconds < 50) return "text-amber-600 dark:text-amber-400";
    return "text-red-600 dark:text-red-400";
  };

  // Format time as MM:SS
  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  };

  // Update filter when URL params change
  useEffect(() => {
    setFilter({ subject: urlSubject, questionType: urlType });
  }, [urlSubject, urlType]);

  // Fetch questions on load
  useEffect(() => {
    fetchQuestions();
  }, [filter]);

  const fetchQuestions = async () => {
    setLoading(true);
    try {
      let url = `${API_BASE}/api/questions?limit=100`;
      if (filter.subject) url += `&subject=${filter.subject}`;
      if (filter.questionType) url += `&question_type=${filter.questionType}`;

      const res = await fetch(url);
      const data = await res.json();

      // Shuffle questions for variety
      const shuffled = data.sort(() => Math.random() - 0.5);
      setQuestions(shuffled);

      if (shuffled.length > 0) {
        setCurrentQuestion(shuffled[0]);
        setCurrentIndex(0);
        setQuestionStartTime(Date.now());
      }
    } catch (err) {
      console.error("Failed to fetch questions:", err);
    }
    setLoading(false);
  };

  const nextQuestion = useCallback(() => {
    setSelectedAnswer(null);
    setResult(null);
    setShowHint(false);
    setQuestionTime(0);
    setLastAnswerTime(null);

    if (currentIndex < questions.length - 1) {
      const nextIdx = currentIndex + 1;
      setCurrentIndex(nextIdx);
      setCurrentQuestion(questions[nextIdx]);
      setQuestionStartTime(Date.now());
    } else {
      // End of questions - shuffle and restart
      const shuffled = [...questions].sort(() => Math.random() - 0.5);
      setQuestions(shuffled);
      setCurrentIndex(0);
      setCurrentQuestion(shuffled[0]);
      setQuestionStartTime(Date.now());
    }
  }, [currentIndex, questions]);

  const submitAnswer = async () => {
    if (selectedAnswer === null || !currentQuestion) return;

    const timeTaken = Math.round((Date.now() - questionStartTime) / 1000);
    setSubmitting(true);

    try {
      const res = await fetch(`${API_BASE}/api/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question_id: currentQuestion.id,
          student_id: "demo-user",
          answer: currentQuestion.options[selectedAnswer],
          time_taken_seconds: timeTaken,
        }),
      });
      const data: AnswerResult = await res.json();
      setResult(data);
      setLastAnswerTime(questionTime);
      setScore((prev) => ({
        correct: prev.correct + (data.is_correct ? 1 : 0),
        total: prev.total + 1,
      }));

      // Update streak
      if (data.is_correct) {
        const newStreak = currentStreak + 1;
        setCurrentStreak(newStreak);
        // Celebrate at milestones: 3, 5, 10, etc.
        if (newStreak >= 3 && (newStreak === 3 || newStreak === 5 || newStreak % 5 === 0)) {
          setShowCelebration(true);
          setTimeout(() => setShowCelebration(false), 2000);
        }
      } else {
        setCurrentStreak(0);
      }

      // Update comprehensive stats for progress page
      updateStats(data.is_correct, currentQuestion);
    } catch (err) {
      console.error("Failed to submit answer:", err);
    }
    setSubmitting(false);
  };

  const updateStats = (isCorrect: boolean, question: Question) => {
    try {
      const savedStats = localStorage.getItem("elevenplustutor_stats");
      const stats = savedStats ? JSON.parse(savedStats) : {
        totalQuestions: 0,
        correctAnswers: 0,
        streak: 0,
        bestStreak: 0,
        lastPractice: null,
        bySubject: {},
        byType: {},
        dailyActivity: {},
      };

      // Update totals
      stats.totalQuestions += 1;
      if (isCorrect) stats.correctAnswers += 1;

      // Update by subject
      if (!stats.bySubject[question.subject]) {
        stats.bySubject[question.subject] = { total: 0, correct: 0 };
      }
      stats.bySubject[question.subject].total += 1;
      if (isCorrect) stats.bySubject[question.subject].correct += 1;

      // Update by type
      if (!stats.byType[question.question_type]) {
        stats.byType[question.question_type] = { total: 0, correct: 0 };
      }
      stats.byType[question.question_type].total += 1;
      if (isCorrect) stats.byType[question.question_type].correct += 1;

      // Update daily activity
      const today = new Date().toISOString().split("T")[0];
      if (!stats.dailyActivity[today]) {
        stats.dailyActivity[today] = { questions: 0, correct: 0 };
      }
      stats.dailyActivity[today].questions += 1;
      if (isCorrect) stats.dailyActivity[today].correct += 1;

      // Update streak
      const todayDate = new Date().toDateString();
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const yesterdayDate = yesterday.toDateString();

      if (stats.lastPractice !== todayDate) {
        if (stats.lastPractice === yesterdayDate || !stats.lastPractice) {
          stats.streak += 1;
        } else {
          stats.streak = 1;
        }
        stats.lastPractice = todayDate;
      }

      if (stats.streak > stats.bestStreak) {
        stats.bestStreak = stats.streak;
      }

      localStorage.setItem("elevenplustutor_stats", JSON.stringify(stats));
    } catch (e) {
      console.error("Error updating stats:", e);
    }
  };

  // Keyboard shortcuts (placed after function declarations)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Don't handle if typing in an input
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;

      // Option selection with A-E keys
      if (!result && currentQuestion) {
        const optionKeys = ['a', 'b', 'c', 'd', 'e'];
        const keyIndex = optionKeys.indexOf(e.key.toLowerCase());
        if (keyIndex !== -1 && keyIndex < currentQuestion.options.length) {
          setSelectedAnswer(keyIndex);
        }
      }

      // Enter to submit or continue
      if (e.key === 'Enter') {
        if (result) {
          nextQuestion();
        } else if (selectedAnswer !== null) {
          submitAnswer();
        }
      }

      // H for hint
      if (e.key.toLowerCase() === 'h' && !result) {
        setShowHint(s => !s);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [result, currentQuestion, selectedAnswer, nextQuestion, submitAnswer]);

  const resetSession = () => {
    setScore({ correct: 0, total: 0 });
    setTimeRemaining(45 * 60);
    setCurrentIndex(0);
    setSelectedAnswer(null);
    setResult(null);
    fetchQuestions();
  };

  const getDifficultyColor = (d: number) => {
    const colors = ["", "text-green-600", "text-green-500", "text-yellow-500", "text-orange-500", "text-red-500"];
    return colors[d] || "text-gray-500";
  };

  const getSubjectColor = (subject: string) => {
    const colors: Record<string, string> = {
      verbal_reasoning: "bg-purple-100 text-purple-800 dark:bg-purple-900/50 dark:text-purple-200",
      non_verbal_reasoning: "bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-200",
      mathematics: "bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-200",
      english: "bg-amber-100 text-amber-800 dark:bg-amber-900/50 dark:text-amber-200",
    };
    return colors[subject] || "bg-gray-100 text-gray-800";
  };

  const getSubjectName = (subject: string) => {
    const names: Record<string, string> = {
      verbal_reasoning: "Verbal Reasoning",
      non_verbal_reasoning: "Non-Verbal Reasoning",
      mathematics: "Mathematics",
      english: "English",
    };
    return names[subject] || subject;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-slate-500 dark:text-slate-400">Loading questions...</p>
        </div>
      </div>
    );
  }

  if (!currentQuestion) {
    return (
      <div className="text-center py-12">
        <Target className="w-16 h-16 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">No Questions Found</h2>
        <p className="text-slate-500 dark:text-slate-400 mb-4">
          {filter.subject || filter.questionType
            ? "Try removing some filters or generate more questions."
            : "Generate some questions to get started."}
        </p>
        <code className="block bg-slate-100 dark:bg-slate-800 p-4 rounded-lg text-sm mb-4 max-w-md mx-auto">
          python scripts/generate_questions.py --count 20
        </code>
        <button
          onClick={() => setFilter({ subject: "", questionType: "" })}
          className="text-blue-600 hover:text-blue-700 font-medium"
        >
          Clear Filters
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header with Stats */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
            {filter.subject ? getSubjectName(filter.subject) : "11+ Practice"}
          </h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm">
            Question {currentIndex + 1} of {questions.length}
          </p>
        </div>

        <div className="flex items-center gap-4">
          {/* Timer Toggle */}
          <button
            onClick={() => setTimerEnabled(!timerEnabled)}
            className={`flex items-center gap-2 px-3 py-2 rounded-lg transition-colors ${
              timerEnabled
                ? "bg-orange-100 text-orange-700 dark:bg-orange-900/50 dark:text-orange-300"
                : "bg-slate-100 text-slate-600 dark:bg-slate-700 dark:text-slate-300"
            }`}
          >
            <Timer className="w-4 h-4" />
            {timerEnabled ? formatTime(timeRemaining) : "Timer Off"}
          </button>

          {/* Score */}
          <div className="flex items-center gap-3 bg-white dark:bg-slate-800 rounded-lg px-4 py-2 shadow-sm border border-slate-200 dark:border-slate-700">
            <div className="text-center">
              <p className="text-2xl font-bold text-slate-900 dark:text-white">{score.correct}</p>
              <p className="text-xs text-slate-500">Correct</p>
            </div>
            <div className="w-px h-8 bg-slate-200 dark:bg-slate-700" />
            <div className="text-center">
              <p className="text-2xl font-bold text-slate-900 dark:text-white">
                {score.total > 0 ? Math.round((score.correct / score.total) * 100) : 0}%
              </p>
              <p className="text-xs text-slate-500">Accuracy</p>
            </div>
          </div>

          {/* Reset */}
          <button
            onClick={resetSession}
            className="p-2 rounded-lg bg-slate-100 text-slate-600 hover:bg-slate-200 dark:bg-slate-700 dark:text-slate-300 dark:hover:bg-slate-600 transition-colors"
            title="Reset Session"
          >
            <RotateCcw className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-2 mb-6">
        <select
          value={filter.subject}
          onChange={(e) => setFilter((f) => ({ ...f, subject: e.target.value }))}
          className="rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white px-3 py-2 text-sm"
        >
          <option value="">All Subjects</option>
          <option value="verbal_reasoning">Verbal Reasoning</option>
          <option value="non_verbal_reasoning">Non-Verbal Reasoning</option>
          <option value="mathematics">Mathematics</option>
          <option value="english">English</option>
        </select>
        <select
          value={filter.questionType}
          onChange={(e) => setFilter((f) => ({ ...f, questionType: e.target.value }))}
          className="rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white px-3 py-2 text-sm"
        >
          <option value="">All Types</option>
          <optgroup label="Verbal Reasoning">
            <option value="synonyms">Synonyms</option>
            <option value="antonyms">Antonyms</option>
            <option value="analogies">Analogies</option>
            <option value="odd_one_out">Odd One Out</option>
            <option value="code_words">Code Words</option>
            <option value="letter_sequences">Letter Sequences</option>
            <option value="hidden_words">Hidden Words</option>
            <option value="compound_words">Compound Words</option>
          </optgroup>
          <optgroup label="Mathematics">
            <option value="arithmetic">Arithmetic</option>
            <option value="fractions">Fractions</option>
            <option value="sequences">Number Sequences</option>
          </optgroup>
          <optgroup label="Non-Verbal Reasoning">
            <option value="nvr_sequences">NVR Sequences</option>
            <option value="nvr_odd_one_out">NVR Odd One Out</option>
            <option value="nvr_analogies">NVR Analogies</option>
          </optgroup>
          <optgroup label="English">
            <option value="comprehension">Comprehension</option>
            <option value="spelling">Spelling</option>
            <option value="grammar">Grammar</option>
          </optgroup>
        </select>
      </div>

      {/* Progress Bar */}
      <div className="h-2 bg-slate-200 dark:bg-slate-700 rounded-full mb-6 overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-300"
          style={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }}
        />
      </div>

      {/* Question Card */}
      <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-lg border border-slate-200 dark:border-slate-700 overflow-hidden">
        {/* Question Header */}
        <div className="bg-slate-50 dark:bg-slate-700/50 px-6 py-4 flex justify-between items-center">
          <div className="flex flex-wrap gap-2">
            <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getSubjectColor(currentQuestion.subject)}`}>
              {getSubjectName(currentQuestion.subject)}
            </span>
            <span className="px-3 py-1 rounded-full text-xs font-medium bg-slate-200 text-slate-700 dark:bg-slate-600 dark:text-slate-200 capitalize">
              {currentQuestion.question_type.replace(/_/g, " ")}
            </span>
          </div>
          <div className="flex items-center gap-4">
            {/* Per-question timer */}
            <div className={`flex items-center gap-1 ${result ? "text-slate-500" : getTimerColor(questionTime)}`}>
              <Clock className="w-4 h-4" />
              <span className="text-sm font-mono font-medium">
                {result && lastAnswerTime !== null ? formatTime(lastAnswerTime) : formatTime(questionTime)}
              </span>
              {!result && questionTime > RECOMMENDED_TIME && (
                <span className="text-xs text-slate-400">(aim for &lt;50s)</span>
              )}
            </div>
            {/* Streak indicator */}
            {currentStreak >= 2 && (
              <div className="flex items-center gap-1 px-2 py-1 bg-orange-100 dark:bg-orange-900/30 rounded-full">
                <span className="text-orange-500">🔥</span>
                <span className="text-xs font-bold text-orange-600 dark:text-orange-400">{currentStreak}</span>
              </div>
            )}
            <div className="flex items-center gap-2">
              <Zap className={`w-4 h-4 ${getDifficultyColor(currentQuestion.difficulty)}`} />
              <span className={`text-sm font-medium ${getDifficultyColor(currentQuestion.difficulty)}`}>
                Level {currentQuestion.difficulty}
              </span>
            </div>
          </div>
        </div>

        {/* Celebration animation */}
        {showCelebration && (
          <div className="bg-gradient-to-r from-yellow-400 via-orange-500 to-red-500 text-white text-center py-2 animate-pulse">
            <span className="text-lg font-bold">🔥 {currentStreak} in a row! Keep going! 🔥</span>
          </div>
        )}

        {/* Question Content */}
        <div className="p-6">
          {/* Render question based on type */}
          {(() => {
            const parsed = parseQuestionText(currentQuestion.question_text, currentQuestion.question_type);

            if (parsed.type === "nvr_sequence" && parsed.sequence) {
              return (
                <div className="mb-8">
                  <p className="text-lg text-slate-900 dark:text-white mb-4">{parsed.instruction}</p>
                  <div className="flex items-center gap-3 flex-wrap justify-center bg-slate-50 dark:bg-slate-700/50 p-4 rounded-xl">
                    {parsed.sequence.map((svg, i) => (
                      <div key={i} className="flex items-center gap-2">
                        <SVGRenderer svg={svg} className="w-16 h-16" />
                        {i < parsed.sequence!.length - 1 && (
                          <ChevronRight className="w-4 h-4 text-slate-400" />
                        )}
                      </div>
                    ))}
                    <ChevronRight className="w-4 h-4 text-slate-400" />
                    <div className="w-16 h-16 border-2 border-dashed border-slate-300 dark:border-slate-500 rounded-lg flex items-center justify-center text-2xl text-slate-400">?</div>
                  </div>
                </div>
              );
            }

            if (parsed.type === "nvr_odd_one_out" && parsed.shapes) {
              return (
                <div className="mb-8">
                  <p className="text-lg text-slate-900 dark:text-white mb-4">{parsed.instruction}</p>
                  <div className="flex items-center gap-4 flex-wrap justify-center bg-slate-50 dark:bg-slate-700/50 p-4 rounded-xl">
                    {parsed.shapes.map((svg, i) => (
                      <div key={i} className="text-center">
                        <SVGRenderer svg={svg} className="w-16 h-16 mx-auto" />
                        <span className="text-sm font-medium text-slate-500 mt-1">{String.fromCharCode(65 + i)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              );
            }

            if (parsed.type === "nvr_analogy" && parsed.pair1) {
              return (
                <div className="mb-8">
                  <p className="text-lg text-slate-900 dark:text-white mb-4">{parsed.instruction}</p>
                  <div className="bg-slate-50 dark:bg-slate-700/50 p-4 rounded-xl">
                    <div className="flex items-center gap-3 justify-center flex-wrap">
                      <SVGRenderer svg={parsed.pair1[0]} className="w-16 h-16" />
                      <span className="text-slate-500 font-medium">is to</span>
                      <SVGRenderer svg={parsed.pair1[1]} className="w-16 h-16" />
                      <span className="text-slate-500 font-medium mx-2">as</span>
                      <SVGRenderer svg={parsed.pair2_first!} className="w-16 h-16" />
                      <span className="text-slate-500 font-medium">is to</span>
                      <div className="w-16 h-16 border-2 border-dashed border-slate-300 dark:border-slate-500 rounded-lg flex items-center justify-center text-2xl text-slate-400">?</div>
                    </div>
                  </div>
                </div>
              );
            }

            if (parsed.type === "comprehension" && parsed.passage) {
              return (
                <div className="mb-8">
                  <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-3">{parsed.title}</h3>
                  <div className="bg-slate-50 dark:bg-slate-700/50 p-4 rounded-xl mb-4 max-h-64 overflow-y-auto">
                    <p className="text-slate-700 dark:text-slate-300 whitespace-pre-line leading-relaxed text-sm">{parsed.passage}</p>
                  </div>
                  <p className="text-lg text-slate-900 dark:text-white font-medium">{parsed.question}</p>
                </div>
              );
            }

            // Default: plain text (with alphabet helper for code words)
            return (
              <div className="mb-8">
                {currentQuestion.question_type === 'code_words' && <AlphabetHelper />}
                <p className="text-lg text-slate-900 dark:text-white whitespace-pre-line leading-relaxed">
                  {currentQuestion.question_text}
                </p>
              </div>
            );
          })()}

          {/* Strategy Tip */}
          {!result && (
            <StrategyTip
              questionType={currentQuestion.question_type}
              show={showHint}
              onToggle={() => setShowHint(s => !s)}
            />
          )}

          {/* Options - handle SVG options for NVR */}
          <div className={`${isSVG(currentQuestion.options[0] || "") ? "grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3" : "space-y-3"}`}>
            {currentQuestion.options.map((option, idx) => {
              const isSelected = selectedAnswer === idx;
              const isCorrect = result && option === result.correct_answer;
              const isWrong = result && isSelected && !result.is_correct;
              const optionIsSVG = isSVG(option);

              return (
                <button
                  key={idx}
                  onClick={() => !result && setSelectedAnswer(idx)}
                  disabled={!!result}
                  className={`${optionIsSVG ? "p-3" : "w-full text-left p-4"} rounded-xl border-2 transition-all duration-200 flex ${optionIsSVG ? "flex-col" : ""} items-center gap-${optionIsSVG ? "2" : "4"} ${
                    result
                      ? isCorrect
                        ? "border-green-500 bg-green-50 dark:bg-green-900/30"
                        : isWrong
                        ? "border-red-500 bg-red-50 dark:bg-red-900/30"
                        : "border-slate-200 dark:border-slate-600 opacity-50"
                      : isSelected
                      ? "border-blue-500 bg-blue-50 dark:bg-blue-900/30 shadow-md"
                      : "border-slate-200 dark:border-slate-600 hover:border-blue-300 hover:bg-slate-50 dark:hover:bg-slate-700/50"
                  }`}
                >
                  {optionIsSVG ? (
                    <>
                      <SVGRenderer svg={option} className="w-14 h-14" />
                      <span
                        className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                          result
                            ? isCorrect
                              ? "bg-green-500 text-white"
                              : isWrong
                              ? "bg-red-500 text-white"
                              : "bg-slate-200 text-slate-600 dark:bg-slate-600 dark:text-slate-300"
                            : isSelected
                            ? "bg-blue-500 text-white"
                            : "bg-slate-200 text-slate-600 dark:bg-slate-600 dark:text-slate-300"
                        }`}
                      >
                        {result ? (
                          isCorrect ? <CheckCircle2 className="w-4 h-4" /> : isWrong ? <XCircle className="w-4 h-4" /> : String.fromCharCode(65 + idx)
                        ) : String.fromCharCode(65 + idx)}
                      </span>
                    </>
                  ) : (
                    <>
                      <span
                        className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                          result
                            ? isCorrect
                              ? "bg-green-500 text-white"
                              : isWrong
                              ? "bg-red-500 text-white"
                              : "bg-slate-200 text-slate-600 dark:bg-slate-600 dark:text-slate-300"
                            : isSelected
                            ? "bg-blue-500 text-white"
                            : "bg-slate-200 text-slate-600 dark:bg-slate-600 dark:text-slate-300"
                        }`}
                      >
                        {result ? (
                          isCorrect ? (
                            <CheckCircle2 className="w-5 h-5" />
                          ) : isWrong ? (
                            <XCircle className="w-5 h-5" />
                          ) : (
                            String.fromCharCode(65 + idx)
                          )
                        ) : (
                          String.fromCharCode(65 + idx)
                        )}
                      </span>
                      <span className="flex-1 text-slate-900 dark:text-white">{option}</span>
                    </>
                  )}
                </button>
              );
            })}
          </div>

          {/* Result Feedback */}
          {result && (
            <div
              className={`mt-6 p-5 rounded-xl ${
                result.is_correct
                  ? "bg-green-100 dark:bg-green-900/30 border border-green-200 dark:border-green-800"
                  : "bg-red-100 dark:bg-red-900/30 border border-red-200 dark:border-red-800"
              }`}
            >
              <div className="flex items-center gap-3 mb-2">
                {result.is_correct ? (
                  <CheckCircle2 className="w-6 h-6 text-green-600 dark:text-green-400" />
                ) : (
                  <XCircle className="w-6 h-6 text-red-600 dark:text-red-400" />
                )}
                <p
                  className={`font-bold text-lg ${
                    result.is_correct
                      ? "text-green-700 dark:text-green-300"
                      : "text-red-700 dark:text-red-300"
                  }`}
                >
                  {result.is_correct ? "Correct!" : "Not quite right"}
                </p>
              </div>
              {result.worked_solution && (
                <div className="mt-3 pt-3 border-t border-current/10">
                  <p className="font-medium text-slate-700 dark:text-slate-300 mb-1">Explanation:</p>
                  <p className="text-slate-600 dark:text-slate-400">{result.worked_solution}</p>
                </div>
              )}
            </div>
          )}

          {/* Actions */}
          <div className="mt-8 flex gap-4">
            {!result ? (
              <button
                onClick={submitAnswer}
                disabled={selectedAnswer === null || submitting}
                className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-slate-400 disabled:to-slate-500 text-white font-semibold py-4 px-6 rounded-xl transition-all shadow-lg hover:shadow-xl disabled:shadow-none flex items-center justify-center gap-2"
              >
                {submitting ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Checking...
                  </>
                ) : (
                  "Submit Answer"
                )}
              </button>
            ) : (
              <button
                onClick={nextQuestion}
                className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-4 px-6 rounded-xl transition-all shadow-lg hover:shadow-xl flex items-center justify-center gap-2"
              >
                Next Question
                <ChevronRight className="w-5 h-5" />
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Keyboard shortcuts hint */}
      <div className="text-center text-sm text-slate-400 dark:text-slate-500 mt-4 space-x-3">
        <span>
          <kbd className="px-1.5 py-0.5 bg-slate-200 dark:bg-slate-700 rounded text-xs font-mono">A</kbd>-
          <kbd className="px-1.5 py-0.5 bg-slate-200 dark:bg-slate-700 rounded text-xs font-mono">E</kbd>
          {" "}select
        </span>
        <span>
          <kbd className="px-1.5 py-0.5 bg-slate-200 dark:bg-slate-700 rounded text-xs font-mono">Enter</kbd>
          {" "}submit
        </span>
        <span>
          <kbd className="px-1.5 py-0.5 bg-slate-200 dark:bg-slate-700 rounded text-xs font-mono">H</kbd>
          {" "}hint
        </span>
      </div>
    </div>
  );
}

export default function PracticePage() {
  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
        </div>
      }
    >
      <PracticeContent />
    </Suspense>
  );
}

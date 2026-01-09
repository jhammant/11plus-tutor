"use client";

import { useState, useEffect, useCallback, Suspense } from "react";
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

  // Timer effect
  useEffect(() => {
    if (!timerEnabled || timeRemaining <= 0) return;

    const interval = setInterval(() => {
      setTimeRemaining((t) => Math.max(0, t - 1));
    }, 1000);

    return () => clearInterval(interval);
  }, [timerEnabled, timeRemaining]);

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
      setScore((prev) => ({
        correct: prev.correct + (data.is_correct ? 1 : 0),
        total: prev.total + 1,
      }));

      // Update comprehensive stats for progress page
      updateStats(data.is_correct, currentQuestion);
    } catch (err) {
      console.error("Failed to submit answer:", err);
    }
    setSubmitting(false);
  };

  const updateStats = (isCorrect: boolean, question: Question) => {
    try {
      const savedStats = localStorage.getItem("examtutor_stats");
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

      localStorage.setItem("examtutor_stats", JSON.stringify(stats));
    } catch (e) {
      console.error("Error updating stats:", e);
    }
  };

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
          <option value="synonyms">Synonyms</option>
          <option value="antonyms">Antonyms</option>
          <option value="analogies">Analogies</option>
          <option value="odd_one_out">Odd One Out</option>
          <option value="code_words">Code Words</option>
          <option value="letter_sequences">Letter Sequences</option>
          <option value="arithmetic">Arithmetic</option>
          <option value="fractions">Fractions</option>
          <option value="sequences">Number Sequences</option>
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
          <div className="flex items-center gap-2">
            <Zap className={`w-4 h-4 ${getDifficultyColor(currentQuestion.difficulty)}`} />
            <span className={`text-sm font-medium ${getDifficultyColor(currentQuestion.difficulty)}`}>
              Level {currentQuestion.difficulty}
            </span>
          </div>
        </div>

        {/* Question Content */}
        <div className="p-6">
          <p className="text-lg text-slate-900 dark:text-white whitespace-pre-line mb-8 leading-relaxed">
            {currentQuestion.question_text}
          </p>

          {/* Options */}
          <div className="space-y-3">
            {currentQuestion.options.map((option, idx) => {
              const isSelected = selectedAnswer === idx;
              const isCorrect = result && option === result.correct_answer;
              const isWrong = result && isSelected && !result.is_correct;

              return (
                <button
                  key={idx}
                  onClick={() => !result && setSelectedAnswer(idx)}
                  disabled={!!result}
                  className={`w-full text-left p-4 rounded-xl border-2 transition-all duration-200 flex items-center gap-4 ${
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

      {/* Keyboard hint */}
      <p className="text-center text-sm text-slate-400 dark:text-slate-500 mt-4">
        Press <kbd className="px-2 py-1 bg-slate-200 dark:bg-slate-700 rounded text-xs">Enter</kbd> to submit
      </p>
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

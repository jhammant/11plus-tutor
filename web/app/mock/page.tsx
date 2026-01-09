"use client";

import { useState, useEffect, useCallback } from "react";
import {
  Clock,
  CheckCircle2,
  XCircle,
  ChevronRight,
  Play,
  Trophy,
  Target,
  AlertCircle,
  BarChart3,
  Timer,
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

interface MockExamResult {
  totalQuestions: number;
  correctAnswers: number;
  timeTaken: number;
  bySubject: {
    [key: string]: { total: number; correct: number };
  };
  answers: { questionId: string; selectedAnswer: string; isCorrect: boolean; correctAnswer: string }[];
  date: string;
}

const API_BASE = "http://localhost:8002";
const EXAM_DURATION = 45 * 60; // 45 minutes in seconds
const EXAM_QUESTIONS = 50; // Number of questions per mock

export default function MockExamPage() {
  const [examState, setExamState] = useState<"setup" | "in_progress" | "review">("setup");
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<{ [key: string]: number }>({});
  const [timeRemaining, setTimeRemaining] = useState(EXAM_DURATION);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<MockExamResult | null>(null);
  const [pastResults, setPastResults] = useState<MockExamResult[]>([]);

  // Load past results
  useEffect(() => {
    try {
      const saved = localStorage.getItem("examtutor_mock_results");
      if (saved) setPastResults(JSON.parse(saved));
    } catch (e) {
      console.error("Error loading results:", e);
    }
  }, []);

  // Timer
  useEffect(() => {
    if (examState !== "in_progress" || timeRemaining <= 0) return;

    const interval = setInterval(() => {
      setTimeRemaining((t) => {
        if (t <= 1) {
          finishExam();
          return 0;
        }
        return t - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [examState, timeRemaining]);

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  };

  const startExam = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/questions?limit=${EXAM_QUESTIONS}`);
      const data = await res.json();

      if (data.length < 10) {
        alert("Not enough questions available for a mock exam. Please generate more questions first.");
        setLoading(false);
        return;
      }

      // Shuffle and select questions
      const shuffled = data.sort(() => Math.random() - 0.5).slice(0, EXAM_QUESTIONS);
      setQuestions(shuffled);
      setAnswers({});
      setTimeRemaining(EXAM_DURATION);
      setCurrentIndex(0);
      setExamState("in_progress");
    } catch (err) {
      console.error("Failed to fetch questions:", err);
      alert("Failed to load questions. Is the backend running?");
    }
    setLoading(false);
  };

  const selectAnswer = (questionId: string, answerIndex: number) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: answerIndex,
    }));
  };

  const goToQuestion = (index: number) => {
    if (index >= 0 && index < questions.length) {
      setCurrentIndex(index);
    }
  };

  const finishExam = useCallback(async () => {
    const timeTaken = EXAM_DURATION - timeRemaining;

    // Calculate results
    const answerResults: MockExamResult["answers"] = [];
    const bySubject: { [key: string]: { total: number; correct: number } } = {};
    let correctCount = 0;

    for (const q of questions) {
      const selectedIdx = answers[q.id];
      const selectedAnswer = selectedIdx !== undefined ? q.options[selectedIdx] : "";

      // Fetch correct answer
      let isCorrect = false;
      let correctAnswer = "";

      try {
        const res = await fetch(`${API_BASE}/api/submit`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            question_id: q.id,
            student_id: "mock-exam",
            answer: selectedAnswer,
            time_taken_seconds: 0,
          }),
        });
        const data = await res.json();
        isCorrect = data.is_correct;
        correctAnswer = data.correct_answer;
      } catch (e) {
        console.error("Error checking answer:", e);
      }

      if (isCorrect) correctCount++;

      answerResults.push({
        questionId: q.id,
        selectedAnswer,
        isCorrect,
        correctAnswer,
      });

      if (!bySubject[q.subject]) {
        bySubject[q.subject] = { total: 0, correct: 0 };
      }
      bySubject[q.subject].total++;
      if (isCorrect) bySubject[q.subject].correct++;
    }

    const examResult: MockExamResult = {
      totalQuestions: questions.length,
      correctAnswers: correctCount,
      timeTaken,
      bySubject,
      answers: answerResults,
      date: new Date().toISOString(),
    };

    setResult(examResult);

    // Save to localStorage
    const updatedResults = [examResult, ...pastResults].slice(0, 10);
    setPastResults(updatedResults);
    localStorage.setItem("examtutor_mock_results", JSON.stringify(updatedResults));

    setExamState("review");
  }, [answers, questions, timeRemaining, pastResults]);

  const getSubjectName = (subject: string) => {
    const names: Record<string, string> = {
      verbal_reasoning: "Verbal Reasoning",
      non_verbal_reasoning: "Non-Verbal Reasoning",
      mathematics: "Mathematics",
      english: "English",
    };
    return names[subject] || subject;
  };

  // Setup screen
  if (examState === "setup") {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-purple-50/20 dark:from-slate-900 dark:via-slate-900 dark:to-slate-800 p-6">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="flex items-center gap-3 mb-8">
            <div className="p-3 rounded-xl bg-gradient-to-br from-orange-500 to-red-600 text-white">
              <Clock className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
                Mock Exams
              </h1>
              <p className="text-sm text-slate-500 dark:text-slate-400">
                Practice under real exam conditions
              </p>
            </div>
          </div>

          {/* Start Exam Card */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-8 border border-slate-200 dark:border-slate-700 shadow-lg mb-8">
            <div className="text-center mb-8">
              <div className="w-20 h-20 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 mx-auto mb-4 flex items-center justify-center">
                <Timer className="w-10 h-10 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
                GL Assessment Style Mock
              </h2>
              <p className="text-slate-500 dark:text-slate-400 max-w-md mx-auto">
                Test yourself with a full-length practice exam. Questions are mixed across all subjects.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-4 mb-8">
              <div className="bg-slate-50 dark:bg-slate-700/50 rounded-xl p-4 text-center">
                <Target className="w-8 h-8 text-blue-500 mx-auto mb-2" />
                <p className="text-2xl font-bold text-slate-900 dark:text-white">{EXAM_QUESTIONS}</p>
                <p className="text-xs text-slate-500 dark:text-slate-400">Questions</p>
              </div>
              <div className="bg-slate-50 dark:bg-slate-700/50 rounded-xl p-4 text-center">
                <Clock className="w-8 h-8 text-orange-500 mx-auto mb-2" />
                <p className="text-2xl font-bold text-slate-900 dark:text-white">45</p>
                <p className="text-xs text-slate-500 dark:text-slate-400">Minutes</p>
              </div>
              <div className="bg-slate-50 dark:bg-slate-700/50 rounded-xl p-4 text-center">
                <Trophy className="w-8 h-8 text-yellow-500 mx-auto mb-2" />
                <p className="text-2xl font-bold text-slate-900 dark:text-white">{EXAM_QUESTIONS}</p>
                <p className="text-xs text-slate-500 dark:text-slate-400">Max Marks</p>
              </div>
            </div>

            <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-4 mb-6">
              <div className="flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-medium text-amber-800 dark:text-amber-200">Exam Conditions</p>
                  <p className="text-sm text-amber-700 dark:text-amber-300">
                    Once started, the timer will begin counting down. Try to complete all questions
                    before time runs out. You can navigate between questions freely.
                  </p>
                </div>
              </div>
            </div>

            <button
              onClick={startExam}
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-slate-400 disabled:to-slate-500 text-white font-semibold py-4 px-6 rounded-xl transition-all shadow-lg hover:shadow-xl disabled:shadow-none flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Loading Questions...
                </>
              ) : (
                <>
                  <Play className="w-5 h-5" />
                  Start Mock Exam
                </>
              )}
            </button>
          </div>

          {/* Past Results */}
          {pastResults.length > 0 && (
            <div className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-200 dark:border-slate-700">
              <h3 className="font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-blue-500" />
                Past Results
              </h3>
              <div className="space-y-3">
                {pastResults.slice(0, 5).map((r, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-700/50 rounded-lg"
                  >
                    <div>
                      <p className="font-medium text-slate-900 dark:text-white">
                        {new Date(r.date).toLocaleDateString("en-GB", {
                          day: "numeric",
                          month: "short",
                          year: "numeric",
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </p>
                      <p className="text-sm text-slate-500 dark:text-slate-400">
                        {r.totalQuestions} questions in {formatTime(r.timeTaken)}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-bold text-slate-900 dark:text-white">
                        {Math.round((r.correctAnswers / r.totalQuestions) * 100)}%
                      </p>
                      <p className="text-sm text-slate-500 dark:text-slate-400">
                        {r.correctAnswers}/{r.totalQuestions}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  // In-progress exam
  if (examState === "in_progress") {
    const currentQ = questions[currentIndex];
    const answeredCount = Object.keys(answers).length;
    const isLowTime = timeRemaining < 300; // 5 minutes

    return (
      <div className="min-h-screen bg-slate-100 dark:bg-slate-900">
        {/* Fixed Header */}
        <div className="fixed top-0 left-0 right-0 bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 z-50 shadow-sm">
          <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <span className="font-semibold text-slate-900 dark:text-white">
                Question {currentIndex + 1} of {questions.length}
              </span>
              <span className="text-sm text-slate-500 dark:text-slate-400">
                {answeredCount} answered
              </span>
            </div>
            <div className="flex items-center gap-4">
              <div
                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-mono font-bold text-lg ${
                  isLowTime
                    ? "bg-red-100 text-red-700 dark:bg-red-900/50 dark:text-red-300 animate-pulse"
                    : "bg-slate-100 text-slate-900 dark:bg-slate-700 dark:text-white"
                }`}
              >
                <Clock className="w-5 h-5" />
                {formatTime(timeRemaining)}
              </div>
              <button
                onClick={finishExam}
                className="px-4 py-2 rounded-lg bg-green-600 hover:bg-green-700 text-white font-medium transition-colors"
              >
                Finish Exam
              </button>
            </div>
          </div>
          {/* Progress bar */}
          <div className="h-1 bg-slate-200 dark:bg-slate-700">
            <div
              className="h-full bg-blue-500 transition-all duration-300"
              style={{ width: `${(answeredCount / questions.length) * 100}%` }}
            />
          </div>
        </div>

        {/* Main Content */}
        <div className="pt-24 pb-32 px-4">
          <div className="max-w-4xl mx-auto">
            {/* Question Card */}
            <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg border border-slate-200 dark:border-slate-700 overflow-hidden">
              <div className="p-6">
                <p className="text-lg text-slate-900 dark:text-white whitespace-pre-line mb-6">
                  {currentQ.question_text}
                </p>

                <div className="space-y-3">
                  {currentQ.options.map((option, idx) => {
                    const isSelected = answers[currentQ.id] === idx;
                    return (
                      <button
                        key={idx}
                        onClick={() => selectAnswer(currentQ.id, idx)}
                        className={`w-full text-left p-4 rounded-lg border-2 transition-all flex items-center gap-4 ${
                          isSelected
                            ? "border-blue-500 bg-blue-50 dark:bg-blue-900/30"
                            : "border-slate-200 dark:border-slate-600 hover:border-blue-300 hover:bg-slate-50 dark:hover:bg-slate-700/50"
                        }`}
                      >
                        <span
                          className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                            isSelected
                              ? "bg-blue-500 text-white"
                              : "bg-slate-200 text-slate-600 dark:bg-slate-600 dark:text-slate-300"
                          }`}
                        >
                          {String.fromCharCode(65 + idx)}
                        </span>
                        <span className="flex-1 text-slate-900 dark:text-white">{option}</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Navigation */}
            <div className="mt-6 flex justify-between">
              <button
                onClick={() => goToQuestion(currentIndex - 1)}
                disabled={currentIndex === 0}
                className="px-6 py-3 rounded-lg bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 font-medium disabled:opacity-50 hover:bg-slate-300 dark:hover:bg-slate-600 transition-colors"
              >
                Previous
              </button>
              <button
                onClick={() => goToQuestion(currentIndex + 1)}
                disabled={currentIndex === questions.length - 1}
                className="px-6 py-3 rounded-lg bg-blue-600 text-white font-medium disabled:opacity-50 hover:bg-blue-700 transition-colors flex items-center gap-2"
              >
                Next
                <ChevronRight className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>

        {/* Question Navigator */}
        <div className="fixed bottom-0 left-0 right-0 bg-white dark:bg-slate-800 border-t border-slate-200 dark:border-slate-700 p-4">
          <div className="max-w-6xl mx-auto">
            <div className="flex flex-wrap gap-2 justify-center">
              {questions.map((q, idx) => {
                const isAnswered = answers[q.id] !== undefined;
                const isCurrent = idx === currentIndex;
                return (
                  <button
                    key={q.id}
                    onClick={() => goToQuestion(idx)}
                    className={`w-9 h-9 rounded-lg text-sm font-medium transition-all ${
                      isCurrent
                        ? "bg-blue-600 text-white ring-2 ring-blue-300"
                        : isAnswered
                        ? "bg-green-100 text-green-700 dark:bg-green-900/50 dark:text-green-300"
                        : "bg-slate-100 text-slate-600 dark:bg-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-600"
                    }`}
                  >
                    {idx + 1}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Review screen
  if (examState === "review" && result) {
    const percentage = Math.round((result.correctAnswers / result.totalQuestions) * 100);
    const grade =
      percentage >= 90
        ? "Excellent"
        : percentage >= 75
        ? "Good"
        : percentage >= 60
        ? "Fair"
        : "Needs Improvement";

    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-purple-50/20 dark:from-slate-900 dark:via-slate-900 dark:to-slate-800 p-6">
        <div className="max-w-4xl mx-auto">
          {/* Results Header */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-8 border border-slate-200 dark:border-slate-700 shadow-lg mb-6 text-center">
            <div className="w-24 h-24 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 mx-auto mb-4 flex items-center justify-center">
              <Trophy className="w-12 h-12 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-slate-900 dark:text-white mb-2">
              Mock Exam Complete!
            </h1>
            <p className="text-slate-500 dark:text-slate-400 mb-6">
              Time taken: {formatTime(result.timeTaken)}
            </p>

            <div className="text-6xl font-bold text-blue-600 dark:text-blue-400 mb-2">
              {percentage}%
            </div>
            <p className="text-xl font-semibold text-slate-700 dark:text-slate-300 mb-2">
              {result.correctAnswers} out of {result.totalQuestions} correct
            </p>
            <span
              className={`inline-block px-4 py-1 rounded-full text-sm font-semibold ${
                percentage >= 75
                  ? "bg-green-100 text-green-700 dark:bg-green-900/50 dark:text-green-300"
                  : percentage >= 60
                  ? "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/50 dark:text-yellow-300"
                  : "bg-red-100 text-red-700 dark:bg-red-900/50 dark:text-red-300"
              }`}
            >
              {grade}
            </span>
          </div>

          {/* Subject Breakdown */}
          <div className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-200 dark:border-slate-700 mb-6">
            <h2 className="font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-blue-500" />
              Performance by Subject
            </h2>
            <div className="space-y-4">
              {Object.entries(result.bySubject).map(([subject, data]) => {
                const subjectPct = Math.round((data.correct / data.total) * 100);
                return (
                  <div key={subject}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-medium text-slate-700 dark:text-slate-300">
                        {getSubjectName(subject)}
                      </span>
                      <span className="text-sm text-slate-500 dark:text-slate-400">
                        {data.correct}/{data.total} ({subjectPct}%)
                      </span>
                    </div>
                    <div className="h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full ${
                          subjectPct >= 75
                            ? "bg-green-500"
                            : subjectPct >= 50
                            ? "bg-yellow-500"
                            : "bg-red-500"
                        }`}
                        style={{ width: `${subjectPct}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Question Review */}
          <div className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-200 dark:border-slate-700 mb-6">
            <h2 className="font-semibold text-slate-900 dark:text-white mb-4">
              Answer Review
            </h2>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {result.answers.map((answer, idx) => (
                <div
                  key={idx}
                  className={`p-3 rounded-lg flex items-center gap-3 ${
                    answer.isCorrect
                      ? "bg-green-50 dark:bg-green-900/20"
                      : "bg-red-50 dark:bg-red-900/20"
                  }`}
                >
                  {answer.isCorrect ? (
                    <CheckCircle2 className="w-5 h-5 text-green-600 dark:text-green-400 flex-shrink-0" />
                  ) : (
                    <XCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0" />
                  )}
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-slate-900 dark:text-white">
                      Question {idx + 1}
                    </p>
                    {!answer.isCorrect && (
                      <p className="text-xs text-slate-500 dark:text-slate-400 truncate">
                        Correct: {answer.correctAnswer}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="flex gap-4">
            <button
              onClick={() => {
                setExamState("setup");
                setResult(null);
              }}
              className="flex-1 bg-slate-200 dark:bg-slate-700 hover:bg-slate-300 dark:hover:bg-slate-600 text-slate-900 dark:text-white font-semibold py-4 px-6 rounded-xl transition-colors"
            >
              Back to Setup
            </button>
            <button
              onClick={startExam}
              className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-4 px-6 rounded-xl transition-all shadow-lg hover:shadow-xl"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return null;
}

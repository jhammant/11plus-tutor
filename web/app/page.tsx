"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import {
  BookOpen,
  Brain,
  Target,
  Zap,
  ArrowRight,
  CheckCircle2,
  Clock,
  Flame,
  Trophy,
  Play,
  Star,
  GraduationCap,
  Sparkles,
  Award,
  Calculator,
  PenTool,
  Puzzle,
} from "lucide-react";

const API_BASE = "http://localhost:8002";

interface Stats {
  total_questions: number;
  subjects: Record<string, { attempted: number; correct: number }>;
}

const SUBJECTS = [
  {
    id: "verbal_reasoning",
    name: "Verbal Reasoning",
    icon: PenTool,
    color: "purple",
    description: "Synonyms, antonyms, analogies, codes",
    gradient: "from-purple-500 to-purple-600",
  },
  {
    id: "non_verbal_reasoning",
    name: "Non-Verbal Reasoning",
    icon: Puzzle,
    color: "blue",
    description: "Patterns, sequences, matrices",
    gradient: "from-blue-500 to-blue-600",
  },
  {
    id: "mathematics",
    name: "Mathematics",
    icon: Calculator,
    color: "green",
    description: "Arithmetic, fractions, word problems",
    gradient: "from-green-500 to-green-600",
  },
  {
    id: "english",
    name: "English",
    icon: BookOpen,
    color: "amber",
    description: "Comprehension, grammar, vocabulary",
    gradient: "from-amber-500 to-amber-600",
  },
];

const QUESTION_TYPES = {
  verbal_reasoning: ["synonyms", "antonyms", "analogies", "odd_one_out", "code_words", "letter_sequences"],
  mathematics: ["arithmetic", "fractions", "sequences", "word_problems"],
};

export default function ElevenPlusTutorHome() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [questionCount, setQuestionCount] = useState(0);
  const [streak, setStreak] = useState(0);

  useEffect(() => {
    // Fetch question count
    fetch(`${API_BASE}/api/questions?limit=1`)
      .then(res => res.json())
      .then(() => {
        // Get total count
        return fetch(`${API_BASE}/api/questions?limit=100`);
      })
      .then(res => res.json())
      .then(data => setQuestionCount(data.length))
      .catch(console.error);

    // Load streak from localStorage
    const savedStreak = localStorage.getItem("elevenplustutor_streak");
    if (savedStreak) setStreak(parseInt(savedStreak));

    // Fetch progress
    fetch(`${API_BASE}/api/progress/demo-user`)
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(console.error);
  }, []);

  const totalAttempted = stats?.subjects
    ? Object.values(stats.subjects).reduce((sum, s) => sum + s.attempted, 0)
    : 0;
  const totalCorrect = stats?.subjects
    ? Object.values(stats.subjects).reduce((sum, s) => sum + s.correct, 0)
    : 0;
  const accuracy = totalAttempted > 0 ? Math.round((totalCorrect / totalAttempted) * 100) : 0;

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="mb-8">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-6">
          <div>
            <h1 className="text-3xl font-bold text-slate-900 dark:text-white">
              11+ Exam Practice
            </h1>
            <p className="text-slate-500 dark:text-slate-400 mt-1">
              Master verbal reasoning, maths, and more for grammar school entrance
            </p>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-4 py-2 bg-orange-100 dark:bg-orange-900/30 rounded-xl">
              <Flame className="w-5 h-5 text-orange-500" />
              <span className="font-bold text-orange-600 dark:text-orange-400">{streak} day streak</span>
            </div>
            <div className="flex items-center gap-2 px-4 py-2 bg-emerald-100 dark:bg-emerald-900/30 rounded-xl">
              <Trophy className="w-5 h-5 text-emerald-500" />
              <span className="font-bold text-emerald-600 dark:text-emerald-400">{accuracy}% accuracy</span>
            </div>
          </div>
        </div>

        {/* Stats Bar */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 border border-slate-200 dark:border-slate-700 shadow-sm">
          <div className="grid grid-cols-3 gap-6">
            <div className="text-center">
              <p className="text-3xl font-bold text-slate-900 dark:text-white">{questionCount}</p>
              <p className="text-sm text-slate-500">Questions Available</p>
            </div>
            <div className="text-center border-x border-slate-200 dark:border-slate-700">
              <p className="text-3xl font-bold text-slate-900 dark:text-white">{totalAttempted}</p>
              <p className="text-sm text-slate-500">Practiced</p>
            </div>
            <div className="text-center">
              <p className="text-3xl font-bold text-emerald-600 dark:text-emerald-400">{totalCorrect}</p>
              <p className="text-sm text-slate-500">Correct</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Start */}
      <div className="mb-8">
        <Link
          href="/practice"
          className="block bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-shadow"
        >
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Play className="w-6 h-6" />
                <span className="font-bold text-xl">Start Practice</span>
              </div>
              <p className="text-blue-100">
                Jump into practice questions and track your progress
              </p>
            </div>
            <ArrowRight className="w-8 h-8" />
          </div>
        </Link>
      </div>

      {/* Subject Cards */}
      <div className="mb-8">
        <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-4">Practice by Subject</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
          {SUBJECTS.map((subject) => {
            const Icon = subject.icon;
            const subjectStats = stats?.subjects?.[subject.id];
            const attempted = subjectStats?.attempted || 0;
            const correct = subjectStats?.correct || 0;

            return (
              <Link
                key={subject.id}
                href={`/practice?subject=${subject.id}`}
                className="bg-white dark:bg-slate-800 rounded-2xl p-6 border border-slate-200 dark:border-slate-700 shadow-sm hover:shadow-md hover:border-slate-300 dark:hover:border-slate-600 transition-all"
              >
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${subject.gradient} flex items-center justify-center mb-4`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="font-bold text-slate-900 dark:text-white mb-1">{subject.name}</h3>
                <p className="text-sm text-slate-500 mb-3">{subject.description}</p>
                {attempted > 0 && (
                  <div className="flex items-center gap-2 text-sm">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                    <span className="text-slate-600 dark:text-slate-400">
                      {correct}/{attempted} correct
                    </span>
                  </div>
                )}
              </Link>
            );
          })}
        </div>
      </div>

      {/* Question Types */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Verbal Reasoning Types */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 shadow-sm overflow-hidden">
          <div className="p-4 border-b border-slate-200 dark:border-slate-700 bg-purple-50 dark:bg-purple-900/20">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-purple-600 flex items-center justify-center">
                <PenTool className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="font-bold text-slate-900 dark:text-white">Verbal Reasoning</h3>
                <p className="text-sm text-slate-500">21 question types in GL exams</p>
              </div>
            </div>
          </div>
          <div className="p-4 grid grid-cols-2 gap-2">
            {["synonyms", "antonyms", "analogies", "odd_one_out", "code_words", "letter_sequences"].map((type) => (
              <Link
                key={type}
                href={`/practice?subject=verbal_reasoning&type=${type}`}
                className="p-3 rounded-lg bg-slate-50 dark:bg-slate-700/50 hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors text-sm font-medium text-slate-700 dark:text-slate-300 capitalize"
              >
                {type.replace("_", " ")}
              </Link>
            ))}
          </div>
        </div>

        {/* Mathematics Types */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 shadow-sm overflow-hidden">
          <div className="p-4 border-b border-slate-200 dark:border-slate-700 bg-green-50 dark:bg-green-900/20">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-green-500 to-green-600 flex items-center justify-center">
                <Calculator className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="font-bold text-slate-900 dark:text-white">Mathematics</h3>
                <p className="text-sm text-slate-500">KS2 curriculum aligned</p>
              </div>
            </div>
          </div>
          <div className="p-4 grid grid-cols-2 gap-2">
            {["arithmetic", "fractions", "sequences", "word_problems", "percentages", "geometry"].map((type) => (
              <Link
                key={type}
                href={`/practice?subject=mathematics&type=${type}`}
                className="p-3 rounded-lg bg-slate-50 dark:bg-slate-700/50 hover:bg-green-50 dark:hover:bg-green-900/20 transition-colors text-sm font-medium text-slate-700 dark:text-slate-300 capitalize"
              >
                {type.replace("_", " ")}
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* Info Section */}
      <div className="mt-8 bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 text-white">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-xl bg-amber-500 flex items-center justify-center flex-shrink-0">
            <GraduationCap className="w-6 h-6 text-white" />
          </div>
          <div>
            <h3 className="font-bold text-lg mb-2">11+ Grammar School Preparation</h3>
            <p className="text-slate-300 text-sm mb-4">
              11+ Tutor helps you prepare for GL Assessment and CEM 11+ exams with AI-generated practice questions,
              instant feedback, and progress tracking. Practice verbal reasoning, non-verbal reasoning, maths, and English.
            </p>
            <div className="flex flex-wrap gap-2">
              <span className="px-3 py-1 bg-white/10 rounded-full text-xs">GL Assessment</span>
              <span className="px-3 py-1 bg-white/10 rounded-full text-xs">CEM</span>
              <span className="px-3 py-1 bg-white/10 rounded-full text-xs">Grammar Schools</span>
              <span className="px-3 py-1 bg-white/10 rounded-full text-xs">Year 5-6</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

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
  Timer,
  Keyboard,
  FileText,
  Lightbulb,
  TrendingUp,
  Route,
  BarChart3,
  Printer,
} from "lucide-react";

const API_BASE = "http://localhost:8002";

interface Stats {
  total_questions: number;
  subjects: Record<string, { attempted: number; correct: number }>;
}

interface LocalStats {
  totalQuestions: number;
  correctAnswers: number;
  streak: number;
  bestStreak: number;
  lastPractice: string | null;
  bySubject: Record<string, { total: number; correct: number }>;
  byType: Record<string, { total: number; correct: number }>;
  dailyActivity: Record<string, { questions: number; correct: number }>;
}

const SUBJECTS = [
  {
    id: "verbal_reasoning",
    name: "Verbal Reasoning",
    icon: PenTool,
    color: "purple",
    description: "Words, codes, analogies",
    gradient: "from-purple-500 to-purple-600",
    types: ["synonyms", "antonyms", "analogies", "odd_one_out", "code_words", "letter_sequences", "hidden_words", "compound_words"],
  },
  {
    id: "non_verbal_reasoning",
    name: "Non-Verbal Reasoning",
    icon: Puzzle,
    color: "blue",
    description: "Shapes, patterns, sequences",
    gradient: "from-blue-500 to-blue-600",
    types: ["nvr_sequences", "nvr_odd_one_out", "nvr_analogies"],
  },
  {
    id: "mathematics",
    name: "Mathematics",
    icon: Calculator,
    color: "green",
    description: "Numbers, fractions, sequences",
    gradient: "from-green-500 to-green-600",
    types: ["arithmetic", "fractions", "sequences"],
  },
  {
    id: "english",
    name: "English",
    icon: BookOpen,
    color: "amber",
    description: "Reading, spelling, grammar",
    gradient: "from-amber-500 to-amber-600",
    types: ["comprehension", "spelling", "grammar"],
  },
];

const QUICK_ACTIONS = [
  {
    name: "Practice Questions",
    description: "Jump into random practice",
    href: "/practice",
    icon: Play,
    gradient: "from-blue-600 to-purple-600",
    primary: true,
  },
  {
    name: "Mock Exam",
    description: "Timed test simulation",
    href: "/mock",
    icon: Timer,
    gradient: "from-orange-500 to-red-500",
  },
  {
    name: "Strategy Guides",
    description: "Learn how to solve each type",
    href: "/strategies",
    icon: Lightbulb,
    gradient: "from-amber-500 to-orange-500",
  },
  {
    name: "Topic Lessons",
    description: "Learn concepts first",
    href: "/learn",
    icon: GraduationCap,
    gradient: "from-emerald-500 to-teal-500",
  },
];

const FEATURES = [
  {
    icon: Timer,
    title: "Per-Question Timer",
    description: "Practice pacing with real exam timing (aim for <50 seconds)",
  },
  {
    icon: Keyboard,
    title: "Keyboard Shortcuts",
    description: "Press A-E to select, Enter to submit, H for hints",
  },
  {
    icon: Flame,
    title: "Streak Tracking",
    description: "Build streaks and see celebrations at milestones",
  },
  {
    icon: Lightbulb,
    title: "Strategy Tips",
    description: "Get hints and strategies for each question type",
  },
  {
    icon: BarChart3,
    title: "Progress Tracking",
    description: "See your improvement over time by subject and type",
  },
  {
    icon: Printer,
    title: "Printable Worksheets",
    description: "Generate PDF worksheets for offline practice",
  },
];

export default function ElevenPlusTutorHome() {
  const [questionCount, setQuestionCount] = useState(0);
  const [localStats, setLocalStats] = useState<LocalStats | null>(null);
  const [todayQuestions, setTodayQuestions] = useState(0);
  const [todayCorrect, setTodayCorrect] = useState(0);
  const [showWelcome, setShowWelcome] = useState(false);

  useEffect(() => {
    // Fetch total question count
    fetch(`${API_BASE}/api/questions/count`)
      .then(res => res.json())
      .then(data => {
        if (data && typeof data.count === 'number') {
          setQuestionCount(data.count);
        }
      })
      .catch(console.error);

    // Load local stats
    const saved = localStorage.getItem("elevenplustutor_stats");
    if (saved) {
      const stats = JSON.parse(saved) as LocalStats;
      setLocalStats(stats);

      // Get today's activity
      const today = new Date().toISOString().split("T")[0];
      if (stats.dailyActivity?.[today]) {
        setTodayQuestions(stats.dailyActivity[today].questions);
        setTodayCorrect(stats.dailyActivity[today].correct);
      }
    }

    // Show welcome modal for first-time visitors
    const hasVisited = localStorage.getItem("elevenplustutor_welcomed");
    if (!hasVisited) {
      setShowWelcome(true);
    }
  }, []);

  const dismissWelcome = () => {
    localStorage.setItem("elevenplustutor_welcomed", "true");
    setShowWelcome(false);
  };

  const streak = localStats?.streak || 0;
  const totalPracticed = localStats?.totalQuestions || 0;
  const totalCorrect = localStats?.correctAnswers || 0;
  const accuracy = totalPracticed > 0 ? Math.round((totalCorrect / totalPracticed) * 100) : 0;
  const dailyGoal = 20;
  const dailyProgress = Math.min(100, Math.round((todayQuestions / dailyGoal) * 100));

  return (
    <div className="space-y-8">
      {/* Welcome Modal for First-Time Visitors */}
      {showWelcome && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-slate-800 rounded-2xl max-w-lg w-full shadow-2xl overflow-hidden">
            {/* Modal Header */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-6 text-white text-center">
              <div className="text-5xl mb-3">🎓</div>
              <h2 className="text-2xl font-bold mb-2">Welcome to 11+ Tutor!</h2>
              <p className="opacity-90">Free practice for grammar school entrance exams</p>
            </div>

            {/* Modal Content */}
            <div className="p-6 space-y-4">
              <div className="flex gap-3 items-start">
                <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center flex-shrink-0">
                  <CheckCircle2 className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                </div>
                <div>
                  <h3 className="font-semibold text-slate-900 dark:text-white">1,364 Verified Questions</h3>
                  <p className="text-sm text-slate-600 dark:text-slate-400">All answers checked by automated tests</p>
                </div>
              </div>

              <div className="flex gap-3 items-start">
                <div className="w-8 h-8 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Target className="w-5 h-5 text-green-600 dark:text-green-400" />
                </div>
                <div>
                  <h3 className="font-semibold text-slate-900 dark:text-white">4 Key Subjects</h3>
                  <p className="text-sm text-slate-600 dark:text-slate-400">Verbal Reasoning, Non-Verbal, Maths, English</p>
                </div>
              </div>

              <div className="flex gap-3 items-start">
                <div className="w-8 h-8 bg-amber-100 dark:bg-amber-900/30 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Sparkles className="w-5 h-5 text-amber-600 dark:text-amber-400" />
                </div>
                <div>
                  <h3 className="font-semibold text-slate-900 dark:text-white">100% Free Forever</h3>
                  <p className="text-sm text-slate-600 dark:text-slate-400">Open source, no subscriptions, runs locally</p>
                </div>
              </div>

              <div className="pt-4 flex flex-col sm:flex-row gap-3">
                <Link
                  href="/getting-started"
                  onClick={dismissWelcome}
                  className="flex-1 py-3 px-4 border-2 border-blue-600 text-blue-600 dark:text-blue-400 font-semibold rounded-xl text-center hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors"
                >
                  Read the Guide
                </Link>
                <button
                  onClick={dismissWelcome}
                  className="flex-1 py-3 px-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-xl hover:shadow-lg transition-all"
                >
                  Start Practicing!
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Header with Daily Goal */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white">
            11+ Exam Practice
          </h1>
          <p className="text-slate-500 dark:text-slate-400 mt-1">
            {(questionCount || 0).toLocaleString()} verified questions across 4 subjects
          </p>
        </div>

        {/* Stats Pills */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2 px-4 py-2 bg-orange-100 dark:bg-orange-900/30 rounded-xl">
            <Flame className="w-5 h-5 text-orange-500" />
            <span className="font-bold text-orange-600 dark:text-orange-400">{streak} day streak</span>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-emerald-100 dark:bg-emerald-900/30 rounded-xl">
            <Trophy className="w-5 h-5 text-emerald-500" />
            <span className="font-bold text-emerald-600 dark:text-emerald-400">{accuracy}% accuracy</span>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-blue-100 dark:bg-blue-900/30 rounded-xl">
            <Target className="w-5 h-5 text-blue-500" />
            <span className="font-bold text-blue-600 dark:text-blue-400">{totalPracticed} practiced</span>
          </div>
        </div>
      </div>

      {/* Daily Goal Progress */}
      <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 border border-slate-200 dark:border-slate-700 shadow-sm">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
              <Target className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900 dark:text-white">Daily Goal</h3>
              <p className="text-sm text-slate-500">{todayQuestions} of {dailyGoal} questions today</p>
            </div>
          </div>
          {todayQuestions >= dailyGoal && (
            <div className="flex items-center gap-2 text-emerald-600 dark:text-emerald-400">
              <CheckCircle2 className="w-5 h-5" />
              <span className="font-semibold">Complete!</span>
            </div>
          )}
        </div>
        <div className="h-3 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
          <div
            className={`h-full transition-all duration-500 ${
              dailyProgress >= 100
                ? "bg-gradient-to-r from-emerald-500 to-green-500"
                : "bg-gradient-to-r from-blue-500 to-purple-500"
            }`}
            style={{ width: `${dailyProgress}%` }}
          />
        </div>
        {todayQuestions > 0 && (
          <p className="text-sm text-slate-500 mt-2">
            {todayCorrect} correct today ({todayQuestions > 0 ? Math.round((todayCorrect / todayQuestions) * 100) : 0}% accuracy)
          </p>
        )}
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-4">Quick Actions</h2>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {QUICK_ACTIONS.map((action) => {
            const Icon = action.icon;
            return (
              <Link
                key={action.name}
                href={action.href}
                className={`${
                  action.primary ? "col-span-2 lg:col-span-1" : ""
                } bg-gradient-to-br ${action.gradient} rounded-2xl p-5 text-white shadow-lg hover:shadow-xl transition-all hover:scale-[1.02]`}
              >
                <Icon className="w-8 h-8 mb-3 opacity-90" />
                <h3 className="font-bold text-lg">{action.name}</h3>
                <p className="text-sm opacity-80">{action.description}</p>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Subject Cards with Question Types */}
      <div>
        <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-4">Practice by Subject</h2>
        <div className="grid md:grid-cols-2 gap-4">
          {SUBJECTS.map((subject) => {
            const Icon = subject.icon;
            const subjectStats = localStats?.bySubject?.[subject.id];
            const attempted = subjectStats?.total || 0;
            const correct = subjectStats?.correct || 0;

            return (
              <div
                key={subject.id}
                className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 shadow-sm overflow-hidden"
              >
                <Link
                  href={`/practice?subject=${subject.id}`}
                  className={`block p-4 border-b border-slate-200 dark:border-slate-700 bg-${subject.color}-50 dark:bg-${subject.color}-900/20 hover:bg-${subject.color}-100 dark:hover:bg-${subject.color}-900/30 transition-colors`}
                  style={{
                    background: subject.color === "purple" ? "rgba(168, 85, 247, 0.1)" :
                               subject.color === "blue" ? "rgba(59, 130, 246, 0.1)" :
                               subject.color === "green" ? "rgba(34, 197, 94, 0.1)" :
                               "rgba(245, 158, 11, 0.1)"
                  }}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${subject.gradient} flex items-center justify-center`}>
                        <Icon className="w-5 h-5 text-white" />
                      </div>
                      <div>
                        <h3 className="font-bold text-slate-900 dark:text-white">{subject.name}</h3>
                        <p className="text-sm text-slate-500">{subject.description}</p>
                      </div>
                    </div>
                    {attempted > 0 && (
                      <div className="text-right">
                        <p className="text-sm font-semibold text-slate-900 dark:text-white">{correct}/{attempted}</p>
                        <p className="text-xs text-slate-500">
                          {Math.round((correct / attempted) * 100)}% correct
                        </p>
                      </div>
                    )}
                  </div>
                </Link>
                <div className="p-3 grid grid-cols-2 gap-2">
                  {subject.types.map((type) => (
                    <Link
                      key={type}
                      href={`/practice?subject=${subject.id}&type=${type}`}
                      className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-700/50 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors text-sm font-medium text-slate-700 dark:text-slate-300"
                    >
                      {type.replace(/_/g, " ").replace(/nvr /g, "").split(' ').map(word =>
                        word.charAt(0).toUpperCase() + word.slice(1)
                      ).join(' ')}
                    </Link>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Features Showcase */}
      <div>
        <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-4">Features</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {FEATURES.map((feature) => {
            const Icon = feature.icon;
            return (
              <div
                key={feature.title}
                className="bg-white dark:bg-slate-800 rounded-xl p-4 border border-slate-200 dark:border-slate-700"
              >
                <Icon className="w-6 h-6 text-blue-500 mb-2" />
                <h3 className="font-semibold text-sm text-slate-900 dark:text-white mb-1">{feature.title}</h3>
                <p className="text-xs text-slate-500">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* More Links */}
      <div className="grid md:grid-cols-3 gap-4">
        <Link
          href="/progress"
          className="bg-white dark:bg-slate-800 rounded-2xl p-5 border border-slate-200 dark:border-slate-700 shadow-sm hover:shadow-md transition-all flex items-center gap-4"
        >
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">
            <TrendingUp className="w-6 h-6 text-white" />
          </div>
          <div>
            <h3 className="font-bold text-slate-900 dark:text-white">View Progress</h3>
            <p className="text-sm text-slate-500">Track your improvement</p>
          </div>
        </Link>

        <Link
          href="/achievements"
          className="bg-white dark:bg-slate-800 rounded-2xl p-5 border border-slate-200 dark:border-slate-700 shadow-sm hover:shadow-md transition-all flex items-center gap-4"
        >
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center">
            <Award className="w-6 h-6 text-white" />
          </div>
          <div>
            <h3 className="font-bold text-slate-900 dark:text-white">Achievements</h3>
            <p className="text-sm text-slate-500">Earn badges and rewards</p>
          </div>
        </Link>

        <Link
          href="/strategies"
          className="bg-white dark:bg-slate-800 rounded-2xl p-5 border border-slate-200 dark:border-slate-700 shadow-sm hover:shadow-md transition-all flex items-center gap-4"
        >
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
            <Lightbulb className="w-6 h-6 text-white" />
          </div>
          <div>
            <h3 className="font-bold text-slate-900 dark:text-white">Strategy Guides</h3>
            <p className="text-sm text-slate-500">Learn solving techniques</p>
          </div>
        </Link>
      </div>

      {/* Info Section */}
      <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 text-white">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-xl bg-amber-500 flex items-center justify-center flex-shrink-0">
            <GraduationCap className="w-6 h-6 text-white" />
          </div>
          <div>
            <h3 className="font-bold text-lg mb-2">Free, Open-Source 11+ Preparation</h3>
            <p className="text-slate-300 text-sm mb-4">
              11+ Tutor is a free, MIT-licensed tool to help every child prepare for grammar school entrance exams.
              All questions are programmatically verified for accuracy. No subscriptions, no hidden costs.
            </p>
            <div className="flex flex-wrap gap-2">
              <span className="px-3 py-1 bg-white/10 rounded-full text-xs">GL Assessment</span>
              <span className="px-3 py-1 bg-white/10 rounded-full text-xs">CEM</span>
              <span className="px-3 py-1 bg-white/10 rounded-full text-xs">{(questionCount || 0).toLocaleString()} Questions</span>
              <span className="px-3 py-1 bg-white/10 rounded-full text-xs">MIT Licensed</span>
              <span className="px-3 py-1 bg-white/10 rounded-full text-xs">Runs Locally</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

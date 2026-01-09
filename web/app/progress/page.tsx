"use client";

import { useState, useEffect } from "react";
import {
  BarChart3,
  TrendingUp,
  Target,
  Calendar,
  Trophy,
  Brain,
  Calculator,
  PenTool,
  Puzzle,
  BookOpen,
  Flame,
  CheckCircle2,
  XCircle,
  Clock,
} from "lucide-react";

interface PracticeStats {
  totalQuestions: number;
  correctAnswers: number;
  streak: number;
  bestStreak: number;
  lastPractice: string | null;
  bySubject: {
    [key: string]: {
      total: number;
      correct: number;
    };
  };
  byType: {
    [key: string]: {
      total: number;
      correct: number;
    };
  };
  dailyActivity: {
    [date: string]: {
      questions: number;
      correct: number;
    };
  };
}

const subjectIcons: { [key: string]: any } = {
  verbal_reasoning: PenTool,
  mathematics: Calculator,
  non_verbal_reasoning: Puzzle,
  english: BookOpen,
};

const subjectNames: { [key: string]: string } = {
  verbal_reasoning: "Verbal Reasoning",
  mathematics: "Mathematics",
  non_verbal_reasoning: "Non-Verbal Reasoning",
  english: "English",
};

export default function ProgressPage() {
  const [stats, setStats] = useState<PracticeStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load stats from localStorage
    const loadStats = () => {
      try {
        const savedStats = localStorage.getItem("examtutor_stats");
        if (savedStats) {
          setStats(JSON.parse(savedStats));
        } else {
          // Initialize empty stats
          setStats({
            totalQuestions: 0,
            correctAnswers: 0,
            streak: 0,
            bestStreak: 0,
            lastPractice: null,
            bySubject: {},
            byType: {},
            dailyActivity: {},
          });
        }
      } catch (e) {
        console.error("Error loading stats:", e);
      }
      setLoading(false);
    };

    loadStats();
  }, []);

  const accuracy = stats && stats.totalQuestions > 0
    ? Math.round((stats.correctAnswers / stats.totalQuestions) * 100)
    : 0;

  const predictedScore = Math.round(accuracy * 0.8 + 20); // Simple prediction formula

  // Get last 7 days activity
  const getLast7Days = () => {
    const days = [];
    for (let i = 6; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      const dateStr = date.toISOString().split("T")[0];
      const dayName = date.toLocaleDateString("en-GB", { weekday: "short" });
      const activity = stats?.dailyActivity?.[dateStr] || { questions: 0, correct: 0 };
      days.push({
        date: dateStr,
        dayName,
        ...activity,
      });
    }
    return days;
  };

  // Get subject performance sorted by accuracy (weakest first)
  const getSubjectPerformance = () => {
    if (!stats?.bySubject) return [];
    return Object.entries(stats.bySubject)
      .map(([subject, data]) => ({
        subject,
        name: subjectNames[subject] || subject,
        total: data.total,
        correct: data.correct,
        accuracy: data.total > 0 ? Math.round((data.correct / data.total) * 100) : 0,
      }))
      .sort((a, b) => a.accuracy - b.accuracy);
  };

  // Get type performance sorted by accuracy (weakest first)
  const getTypePerformance = () => {
    if (!stats?.byType) return [];
    return Object.entries(stats.byType)
      .map(([type, data]) => ({
        type,
        name: type.split("_").map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(" "),
        total: data.total,
        correct: data.correct,
        accuracy: data.total > 0 ? Math.round((data.correct / data.total) * 100) : 0,
      }))
      .sort((a, b) => a.accuracy - b.accuracy);
  };

  const last7Days = getLast7Days();
  const subjectPerf = getSubjectPerformance();
  const typePerf = getTypePerformance();
  const maxQuestions = Math.max(...last7Days.map(d => d.questions), 10);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-purple-50/20 dark:from-slate-900 dark:via-slate-900 dark:to-slate-800 p-6">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center gap-3 mb-8">
          <div className="p-3 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 text-white">
            <BarChart3 className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
              My Progress
            </h1>
            <p className="text-sm text-slate-500 dark:text-slate-400">
              Track your learning journey
            </p>
          </div>
        </div>

        {/* Key Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {/* Total Questions */}
          <div className="bg-white dark:bg-slate-800 rounded-xl p-5 border border-slate-200 dark:border-slate-700 shadow-sm">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-blue-100 dark:bg-blue-900/30">
                <Target className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <div className="text-2xl font-bold text-slate-900 dark:text-white">
                  {stats?.totalQuestions || 0}
                </div>
                <div className="text-xs text-slate-500 dark:text-slate-400">
                  Questions Practiced
                </div>
              </div>
            </div>
          </div>

          {/* Accuracy */}
          <div className="bg-white dark:bg-slate-800 rounded-xl p-5 border border-slate-200 dark:border-slate-700 shadow-sm">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-green-100 dark:bg-green-900/30">
                <CheckCircle2 className="w-5 h-5 text-green-600 dark:text-green-400" />
              </div>
              <div>
                <div className="text-2xl font-bold text-slate-900 dark:text-white">
                  {accuracy}%
                </div>
                <div className="text-xs text-slate-500 dark:text-slate-400">
                  Overall Accuracy
                </div>
              </div>
            </div>
          </div>

          {/* Current Streak */}
          <div className="bg-white dark:bg-slate-800 rounded-xl p-5 border border-slate-200 dark:border-slate-700 shadow-sm">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-orange-100 dark:bg-orange-900/30">
                <Flame className="w-5 h-5 text-orange-600 dark:text-orange-400" />
              </div>
              <div>
                <div className="text-2xl font-bold text-slate-900 dark:text-white">
                  {stats?.streak || 0}
                </div>
                <div className="text-xs text-slate-500 dark:text-slate-400">
                  Day Streak
                </div>
              </div>
            </div>
          </div>

          {/* Predicted Score */}
          <div className="bg-white dark:bg-slate-800 rounded-xl p-5 border border-slate-200 dark:border-slate-700 shadow-sm">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-purple-100 dark:bg-purple-900/30">
                <Trophy className="w-5 h-5 text-purple-600 dark:text-purple-400" />
              </div>
              <div>
                <div className="text-2xl font-bold text-slate-900 dark:text-white">
                  {stats?.totalQuestions ? predictedScore : "-"}
                </div>
                <div className="text-xs text-slate-500 dark:text-slate-400">
                  Predicted Score
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Activity Chart & Subject Performance */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Last 7 Days Activity */}
          <div className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-200 dark:border-slate-700 shadow-sm">
            <h2 className="font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
              <Calendar className="w-5 h-5 text-blue-500" />
              Last 7 Days
            </h2>
            <div className="flex items-end justify-between gap-2 h-40">
              {last7Days.map((day) => (
                <div key={day.date} className="flex-1 flex flex-col items-center gap-2">
                  <div className="w-full flex flex-col items-center justify-end h-28">
                    <div
                      className="w-full max-w-8 rounded-t-md bg-gradient-to-t from-blue-500 to-blue-400 transition-all duration-300"
                      style={{
                        height: `${Math.max((day.questions / maxQuestions) * 100, day.questions > 0 ? 10 : 0)}%`,
                        minHeight: day.questions > 0 ? "8px" : "0"
                      }}
                    ></div>
                  </div>
                  <span className="text-xs text-slate-500 dark:text-slate-400">
                    {day.dayName}
                  </span>
                  <span className="text-xs font-medium text-slate-700 dark:text-slate-300">
                    {day.questions}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Subject Performance */}
          <div className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-200 dark:border-slate-700 shadow-sm">
            <h2 className="font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
              <Brain className="w-5 h-5 text-purple-500" />
              Subject Performance
            </h2>
            {subjectPerf.length > 0 ? (
              <div className="space-y-4">
                {subjectPerf.map((item) => {
                  const Icon = subjectIcons[item.subject] || Brain;
                  const isWeak = item.accuracy < 70;
                  return (
                    <div key={item.subject}>
                      <div className="flex items-center justify-between mb-1">
                        <div className="flex items-center gap-2">
                          <Icon className={`w-4 h-4 ${isWeak ? "text-red-500" : "text-slate-400"}`} />
                          <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                            {item.name}
                          </span>
                          {isWeak && (
                            <span className="text-xs px-2 py-0.5 rounded-full bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400">
                              Needs work
                            </span>
                          )}
                        </div>
                        <span className="text-sm font-semibold text-slate-900 dark:text-white">
                          {item.accuracy}%
                        </span>
                      </div>
                      <div className="w-full h-2 bg-slate-100 dark:bg-slate-700 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full transition-all duration-300 ${
                            item.accuracy >= 80 ? "bg-green-500" :
                            item.accuracy >= 70 ? "bg-blue-500" :
                            item.accuracy >= 50 ? "bg-yellow-500" : "bg-red-500"
                          }`}
                          style={{ width: `${item.accuracy}%` }}
                        ></div>
                      </div>
                      <div className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                        {item.correct}/{item.total} correct
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="text-center py-8 text-slate-500 dark:text-slate-400">
                <Brain className="w-12 h-12 mx-auto mb-2 opacity-30" />
                <p>Start practicing to see your progress!</p>
              </div>
            )}
          </div>
        </div>

        {/* Question Type Performance */}
        <div className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-200 dark:border-slate-700 shadow-sm">
          <h2 className="font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-green-500" />
            Performance by Question Type
          </h2>
          {typePerf.length > 0 ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {typePerf.map((item) => {
                const isWeak = item.accuracy < 70;
                return (
                  <div
                    key={item.type}
                    className={`p-4 rounded-lg border ${
                      isWeak
                        ? "bg-red-50 dark:bg-red-900/10 border-red-200 dark:border-red-800"
                        : "bg-slate-50 dark:bg-slate-700/50 border-slate-200 dark:border-slate-600"
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                        {item.name}
                      </span>
                      {isWeak ? (
                        <XCircle className="w-4 h-4 text-red-500" />
                      ) : (
                        <CheckCircle2 className="w-4 h-4 text-green-500" />
                      )}
                    </div>
                    <div className="flex items-end gap-2">
                      <span className={`text-2xl font-bold ${
                        isWeak ? "text-red-600 dark:text-red-400" : "text-slate-900 dark:text-white"
                      }`}>
                        {item.accuracy}%
                      </span>
                      <span className="text-xs text-slate-500 dark:text-slate-400 mb-1">
                        ({item.correct}/{item.total})
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center py-8 text-slate-500 dark:text-slate-400">
              <Target className="w-12 h-12 mx-auto mb-2 opacity-30" />
              <p>Complete some questions to see your performance breakdown!</p>
            </div>
          )}
        </div>

        {/* Recommendations */}
        {subjectPerf.filter(s => s.accuracy < 70).length > 0 && (
          <div className="bg-gradient-to-r from-orange-500/10 to-red-500/10 rounded-xl p-6 border border-orange-200 dark:border-orange-800">
            <h2 className="font-semibold text-slate-900 dark:text-white mb-3 flex items-center gap-2">
              <Target className="w-5 h-5 text-orange-500" />
              Recommended Focus Areas
            </h2>
            <div className="flex flex-wrap gap-2">
              {subjectPerf
                .filter(s => s.accuracy < 70)
                .map((item) => (
                  <a
                    key={item.subject}
                    href={`/practice?subject=${item.subject}`}
                    className="px-4 py-2 rounded-lg bg-white dark:bg-slate-800 border border-orange-300 dark:border-orange-700 text-sm font-medium text-orange-700 dark:text-orange-300 hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-colors"
                  >
                    Practice {item.name}
                  </a>
                ))}
            </div>
          </div>
        )}

        {/* Empty State CTA */}
        {stats?.totalQuestions === 0 && (
          <div className="text-center py-12">
            <div className="w-20 h-20 rounded-full bg-blue-100 dark:bg-blue-900/30 mx-auto mb-4 flex items-center justify-center">
              <Target className="w-10 h-10 text-blue-500" />
            </div>
            <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-2">
              Start Your Learning Journey!
            </h2>
            <p className="text-slate-500 dark:text-slate-400 mb-6 max-w-md mx-auto">
              Answer practice questions to track your progress and identify areas for improvement.
            </p>
            <a
              href="/practice"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold hover:shadow-lg hover:shadow-blue-500/25 transition-all"
            >
              <Target className="w-5 h-5" />
              Start Practicing
            </a>
          </div>
        )}
      </div>
    </div>
  );
}

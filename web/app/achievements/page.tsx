"use client";

import { useState, useEffect } from "react";
import {
  Trophy,
  Target,
  Zap,
  Flame,
  Star,
  Award,
  BookOpen,
  Clock,
  CheckCircle2,
  Lock,
  Sparkles,
} from "lucide-react";

interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: any;
  color: string;
  requirement: number;
  type: "questions" | "streak" | "accuracy" | "speed" | "subject";
  subject?: string;
}

const achievements: Achievement[] = [
  {
    id: "first_question",
    name: "First Steps",
    description: "Answer your first question",
    icon: Star,
    color: "from-yellow-400 to-yellow-600",
    requirement: 1,
    type: "questions",
  },
  {
    id: "ten_questions",
    name: "Getting Started",
    description: "Answer 10 questions",
    icon: Target,
    color: "from-blue-400 to-blue-600",
    requirement: 10,
    type: "questions",
  },
  {
    id: "fifty_questions",
    name: "Dedicated Learner",
    description: "Answer 50 questions",
    icon: BookOpen,
    color: "from-green-400 to-green-600",
    requirement: 50,
    type: "questions",
  },
  {
    id: "hundred_questions",
    name: "Century Club",
    description: "Answer 100 questions",
    icon: Trophy,
    color: "from-purple-400 to-purple-600",
    requirement: 100,
    type: "questions",
  },
  {
    id: "five_hundred_questions",
    name: "Quiz Master",
    description: "Answer 500 questions",
    icon: Award,
    color: "from-red-400 to-red-600",
    requirement: 500,
    type: "questions",
  },
  {
    id: "streak_3",
    name: "On a Roll",
    description: "Maintain a 3-day streak",
    icon: Flame,
    color: "from-orange-400 to-orange-600",
    requirement: 3,
    type: "streak",
  },
  {
    id: "streak_7",
    name: "Week Warrior",
    description: "Maintain a 7-day streak",
    icon: Flame,
    color: "from-orange-500 to-red-500",
    requirement: 7,
    type: "streak",
  },
  {
    id: "streak_30",
    name: "Monthly Champion",
    description: "Maintain a 30-day streak",
    icon: Flame,
    color: "from-red-500 to-pink-600",
    requirement: 30,
    type: "streak",
  },
  {
    id: "accuracy_70",
    name: "Sharp Mind",
    description: "Achieve 70% overall accuracy (min 20 questions)",
    icon: Zap,
    color: "from-cyan-400 to-cyan-600",
    requirement: 70,
    type: "accuracy",
  },
  {
    id: "accuracy_80",
    name: "Precision Expert",
    description: "Achieve 80% overall accuracy (min 50 questions)",
    icon: Zap,
    color: "from-teal-400 to-teal-600",
    requirement: 80,
    type: "accuracy",
  },
  {
    id: "accuracy_90",
    name: "Near Perfect",
    description: "Achieve 90% overall accuracy (min 100 questions)",
    icon: Sparkles,
    color: "from-amber-400 to-amber-600",
    requirement: 90,
    type: "accuracy",
  },
  {
    id: "vr_master",
    name: "Verbal Virtuoso",
    description: "Answer 100 Verbal Reasoning questions",
    icon: BookOpen,
    color: "from-violet-400 to-violet-600",
    requirement: 100,
    type: "subject",
    subject: "verbal_reasoning",
  },
  {
    id: "maths_master",
    name: "Maths Maestro",
    description: "Answer 100 Mathematics questions",
    icon: Target,
    color: "from-emerald-400 to-emerald-600",
    requirement: 100,
    type: "subject",
    subject: "mathematics",
  },
];

interface Stats {
  totalQuestions: number;
  correctAnswers: number;
  streak: number;
  bestStreak: number;
  bySubject: { [key: string]: { total: number; correct: number } };
}

export default function AchievementsPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [unlockedAchievements, setUnlockedAchievements] = useState<Set<string>>(new Set());

  useEffect(() => {
    // Load stats
    try {
      const savedStats = localStorage.getItem("elevenplustutor_stats");
      if (savedStats) {
        setStats(JSON.parse(savedStats));
      } else {
        setStats({
          totalQuestions: 0,
          correctAnswers: 0,
          streak: 0,
          bestStreak: 0,
          bySubject: {},
        });
      }

      // Load unlocked achievements
      const savedAchievements = localStorage.getItem("elevenplustutor_achievements");
      if (savedAchievements) {
        setUnlockedAchievements(new Set(JSON.parse(savedAchievements)));
      }
    } catch (e) {
      console.error("Error loading data:", e);
    }
  }, []);

  // Check and update achievements
  useEffect(() => {
    if (!stats) return;

    const newUnlocked = new Set(unlockedAchievements);
    let changed = false;

    for (const achievement of achievements) {
      if (newUnlocked.has(achievement.id)) continue;

      let isUnlocked = false;

      switch (achievement.type) {
        case "questions":
          isUnlocked = stats.totalQuestions >= achievement.requirement;
          break;
        case "streak":
          isUnlocked = stats.bestStreak >= achievement.requirement;
          break;
        case "accuracy":
          const accuracy = stats.totalQuestions > 0
            ? (stats.correctAnswers / stats.totalQuestions) * 100
            : 0;
          const minQuestions =
            achievement.requirement === 70 ? 20 : achievement.requirement === 80 ? 50 : 100;
          isUnlocked = accuracy >= achievement.requirement && stats.totalQuestions >= minQuestions;
          break;
        case "subject":
          if (achievement.subject && stats.bySubject[achievement.subject]) {
            isUnlocked = stats.bySubject[achievement.subject].total >= achievement.requirement;
          }
          break;
      }

      if (isUnlocked) {
        newUnlocked.add(achievement.id);
        changed = true;
      }
    }

    if (changed) {
      setUnlockedAchievements(newUnlocked);
      localStorage.setItem("elevenplustutor_achievements", JSON.stringify([...newUnlocked]));
    }
  }, [stats, unlockedAchievements]);

  const getProgress = (achievement: Achievement): number => {
    if (!stats) return 0;

    switch (achievement.type) {
      case "questions":
        return Math.min((stats.totalQuestions / achievement.requirement) * 100, 100);
      case "streak":
        return Math.min((stats.bestStreak / achievement.requirement) * 100, 100);
      case "accuracy":
        const accuracy = stats.totalQuestions > 0
          ? (stats.correctAnswers / stats.totalQuestions) * 100
          : 0;
        return Math.min((accuracy / achievement.requirement) * 100, 100);
      case "subject":
        if (achievement.subject && stats.bySubject[achievement.subject]) {
          return Math.min(
            (stats.bySubject[achievement.subject].total / achievement.requirement) * 100,
            100
          );
        }
        return 0;
      default:
        return 0;
    }
  };

  const getProgressText = (achievement: Achievement): string => {
    if (!stats) return "0";

    switch (achievement.type) {
      case "questions":
        return `${stats.totalQuestions}/${achievement.requirement}`;
      case "streak":
        return `${stats.bestStreak}/${achievement.requirement}`;
      case "accuracy":
        const accuracy = stats.totalQuestions > 0
          ? Math.round((stats.correctAnswers / stats.totalQuestions) * 100)
          : 0;
        return `${accuracy}%/${achievement.requirement}%`;
      case "subject":
        if (achievement.subject && stats.bySubject[achievement.subject]) {
          return `${stats.bySubject[achievement.subject].total}/${achievement.requirement}`;
        }
        return `0/${achievement.requirement}`;
      default:
        return "0";
    }
  };

  const unlockedCount = unlockedAchievements.size;
  const totalCount = achievements.length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-purple-50/20 dark:from-slate-900 dark:via-slate-900 dark:to-slate-800 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <div className="p-3 rounded-xl bg-gradient-to-br from-yellow-500 to-orange-600 text-white">
              <Trophy className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
                Achievements
              </h1>
              <p className="text-sm text-slate-500 dark:text-slate-400">
                Track your milestones and rewards
              </p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold text-slate-900 dark:text-white">
              {unlockedCount}/{totalCount}
            </div>
            <p className="text-sm text-slate-500 dark:text-slate-400">Unlocked</p>
          </div>
        </div>

        {/* Progress Overview */}
        <div className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-200 dark:border-slate-700 mb-6">
          <div className="flex items-center justify-between mb-2">
            <span className="font-medium text-slate-700 dark:text-slate-300">
              Overall Progress
            </span>
            <span className="text-sm text-slate-500 dark:text-slate-400">
              {Math.round((unlockedCount / totalCount) * 100)}%
            </span>
          </div>
          <div className="h-3 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-yellow-500 to-orange-500 rounded-full transition-all duration-500"
              style={{ width: `${(unlockedCount / totalCount) * 100}%` }}
            />
          </div>
        </div>

        {/* Achievements Grid */}
        <div className="grid md:grid-cols-2 gap-4">
          {achievements.map((achievement) => {
            const Icon = achievement.icon;
            const isUnlocked = unlockedAchievements.has(achievement.id);
            const progress = getProgress(achievement);

            return (
              <div
                key={achievement.id}
                className={`relative overflow-hidden rounded-xl border ${
                  isUnlocked
                    ? "bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700"
                    : "bg-slate-100 dark:bg-slate-800/50 border-slate-200 dark:border-slate-700/50"
                }`}
              >
                {/* Unlocked glow effect */}
                {isUnlocked && (
                  <div className="absolute inset-0 bg-gradient-to-r from-yellow-500/5 to-orange-500/5" />
                )}

                <div className="relative p-4 flex items-start gap-4">
                  {/* Icon */}
                  <div
                    className={`w-14 h-14 rounded-xl flex items-center justify-center flex-shrink-0 ${
                      isUnlocked
                        ? `bg-gradient-to-br ${achievement.color} text-white shadow-lg`
                        : "bg-slate-200 dark:bg-slate-700 text-slate-400 dark:text-slate-500"
                    }`}
                  >
                    {isUnlocked ? (
                      <Icon className="w-7 h-7" />
                    ) : (
                      <Lock className="w-6 h-6" />
                    )}
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <h3
                        className={`font-semibold ${
                          isUnlocked
                            ? "text-slate-900 dark:text-white"
                            : "text-slate-500 dark:text-slate-400"
                        }`}
                      >
                        {achievement.name}
                      </h3>
                      {isUnlocked && (
                        <CheckCircle2 className="w-4 h-4 text-green-500 flex-shrink-0" />
                      )}
                    </div>
                    <p
                      className={`text-sm mb-2 ${
                        isUnlocked
                          ? "text-slate-600 dark:text-slate-400"
                          : "text-slate-400 dark:text-slate-500"
                      }`}
                    >
                      {achievement.description}
                    </p>

                    {/* Progress bar */}
                    {!isUnlocked && (
                      <div>
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs text-slate-500 dark:text-slate-400">
                            Progress
                          </span>
                          <span className="text-xs font-medium text-slate-600 dark:text-slate-400">
                            {getProgressText(achievement)}
                          </span>
                        </div>
                        <div className="h-1.5 bg-slate-200 dark:bg-slate-600 rounded-full overflow-hidden">
                          <div
                            className={`h-full bg-gradient-to-r ${achievement.color} rounded-full transition-all duration-300`}
                            style={{ width: `${progress}%` }}
                          />
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Empty State */}
        {unlockedCount === 0 && (
          <div className="mt-8 text-center py-12 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700">
            <Trophy className="w-16 h-16 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">
              Start Your Journey!
            </h2>
            <p className="text-slate-500 dark:text-slate-400 mb-6 max-w-md mx-auto">
              Practice questions to unlock achievements and track your progress.
            </p>
            <a
              href="/practice"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold hover:shadow-lg transition-all"
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

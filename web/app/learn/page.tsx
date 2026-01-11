"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import {
  BookOpen,
  GraduationCap,
  PenTool,
  Calculator,
  Puzzle,
  ChevronRight,
  CheckCircle2,
  Lock,
  Play,
  Sparkles,
} from "lucide-react";

const API_BASE = "http://localhost:8002";

interface Topic {
  id: string;
  name: string;
  lesson_count: number;
}

interface Subject {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  topics: Topic[];
}

const iconMap: Record<string, any> = {
  PenTool,
  Calculator,
  Puzzle,
  BookOpen,
};

const colorClasses: Record<string, { bg: string; text: string; border: string; gradient: string }> = {
  purple: {
    bg: "bg-purple-100 dark:bg-purple-900/30",
    text: "text-purple-600 dark:text-purple-400",
    border: "border-purple-200 dark:border-purple-800",
    gradient: "from-purple-500 to-purple-600",
  },
  green: {
    bg: "bg-green-100 dark:bg-green-900/30",
    text: "text-green-600 dark:text-green-400",
    border: "border-green-200 dark:border-green-800",
    gradient: "from-green-500 to-green-600",
  },
  blue: {
    bg: "bg-blue-100 dark:bg-blue-900/30",
    text: "text-blue-600 dark:text-blue-400",
    border: "border-blue-200 dark:border-blue-800",
    gradient: "from-blue-500 to-blue-600",
  },
  amber: {
    bg: "bg-amber-100 dark:bg-amber-900/30",
    text: "text-amber-600 dark:text-amber-400",
    border: "border-amber-200 dark:border-amber-800",
    gradient: "from-amber-500 to-amber-600",
  },
};

export default function LearnPage() {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedSubject, setExpandedSubject] = useState<string | null>("verbal_reasoning");

  useEffect(() => {
    fetch(`${API_BASE}/api/learn/subjects`)
      .then((res) => res.json())
      .then((data) => {
        setSubjects(data.subjects || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error loading subjects:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center">
            <GraduationCap className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
              Learn
            </h1>
            <p className="text-slate-500 dark:text-slate-400">
              Master the concepts before practicing
            </p>
          </div>
        </div>
      </div>

      {/* Learning Path Banner */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl p-6 mb-8 text-white">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="w-5 h-5" />
              <span className="text-sm font-medium text-indigo-200">Learning Philosophy</span>
            </div>
            <h2 className="text-xl font-bold mb-2">Understand First, Practice Second</h2>
            <p className="text-indigo-100 text-sm">
              Each lesson teaches you the concept and strategies. Once you understand the approach,
              you'll solve questions faster and more confidently.
            </p>
          </div>
        </div>
      </div>

      {/* Subject Cards */}
      <div className="space-y-4">
        {subjects.map((subject) => {
          const Icon = iconMap[subject.icon] || BookOpen;
          const colors = colorClasses[subject.color] || colorClasses.blue;
          const isExpanded = expandedSubject === subject.id;
          const totalLessons = subject.topics.reduce((sum, t) => sum + t.lesson_count, 0);
          const availableTopics = subject.topics.filter((t) => t.lesson_count > 0);

          return (
            <div
              key={subject.id}
              className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden"
            >
              {/* Subject Header */}
              <button
                onClick={() => setExpandedSubject(isExpanded ? null : subject.id)}
                className="w-full px-6 py-5 flex items-center justify-between hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors"
              >
                <div className="flex items-center gap-4">
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${colors.gradient} flex items-center justify-center`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <div className="text-left">
                    <h3 className="font-bold text-slate-900 dark:text-white">{subject.name}</h3>
                    <p className="text-sm text-slate-500">{subject.description}</p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <p className="text-sm font-medium text-slate-900 dark:text-white">
                      {totalLessons} lessons
                    </p>
                    <p className="text-xs text-slate-500">
                      {subject.topics.length} topics
                    </p>
                  </div>
                  <ChevronRight
                    className={`w-5 h-5 text-slate-400 transition-transform ${
                      isExpanded ? "rotate-90" : ""
                    }`}
                  />
                </div>
              </button>

              {/* Topics List */}
              {isExpanded && (
                <div className="px-6 pb-5 border-t border-slate-200 dark:border-slate-700">
                  <div className="pt-4 space-y-2">
                    {subject.topics.map((topic) => {
                      const hasContent = topic.lesson_count > 0;

                      return (
                        <Link
                          key={topic.id}
                          href={hasContent ? `/learn/${subject.id}/${topic.id}` : "#"}
                          className={`flex items-center justify-between p-4 rounded-lg transition-colors ${
                            hasContent
                              ? "bg-slate-50 dark:bg-slate-700/50 hover:bg-slate-100 dark:hover:bg-slate-700"
                              : "bg-slate-50/50 dark:bg-slate-800/50 opacity-60 cursor-not-allowed"
                          }`}
                        >
                          <div className="flex items-center gap-3">
                            {hasContent ? (
                              <div className={`w-8 h-8 rounded-lg ${colors.bg} ${colors.text} flex items-center justify-center`}>
                                <Play className="w-4 h-4" />
                              </div>
                            ) : (
                              <div className="w-8 h-8 rounded-lg bg-slate-200 dark:bg-slate-600 flex items-center justify-center">
                                <Lock className="w-4 h-4 text-slate-400" />
                              </div>
                            )}
                            <div>
                              <h4 className={`font-medium ${hasContent ? "text-slate-900 dark:text-white" : "text-slate-400"}`}>
                                {topic.name}
                              </h4>
                              {!hasContent && (
                                <p className="text-xs text-slate-400">Coming soon</p>
                              )}
                            </div>
                          </div>
                          {hasContent && (
                            <ChevronRight className="w-4 h-4 text-slate-400" />
                          )}
                        </Link>
                      );
                    })}
                  </div>

                  {/* Quick Practice Link */}
                  {availableTopics.length > 0 && (
                    <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-700">
                      <Link
                        href={`/practice?subject=${subject.id}`}
                        className={`inline-flex items-center gap-2 text-sm font-medium ${colors.text} hover:underline`}
                      >
                        Practice all {subject.name} questions
                        <ChevronRight className="w-4 h-4" />
                      </Link>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Strategies Link */}
      <div className="mt-8 bg-amber-50 dark:bg-amber-900/20 rounded-xl p-6 border border-amber-200 dark:border-amber-800">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center flex-shrink-0">
            <BookOpen className="w-6 h-6 text-white" />
          </div>
          <div>
            <h3 className="font-bold text-slate-900 dark:text-white mb-1">
              Looking for strategy guides?
            </h3>
            <p className="text-sm text-slate-600 dark:text-slate-400 mb-3">
              Our strategy guides teach you exactly how to approach each question type,
              with step-by-step methods and worked examples.
            </p>
            <Link
              href="/strategies"
              className="inline-flex items-center gap-2 text-sm font-medium text-amber-600 dark:text-amber-400 hover:underline"
            >
              View all strategy guides
              <ChevronRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

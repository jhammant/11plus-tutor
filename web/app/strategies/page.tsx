"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import {
  Lightbulb,
  PenTool,
  Calculator,
  Puzzle,
  BookOpen,
  ChevronRight,
  Target,
  Clock,
  AlertTriangle,
} from "lucide-react";

const API_BASE = "http://localhost:8002";

interface Strategy {
  question_type: string;
  subject: string;
  title: string;
  is_free: boolean;
  difficulty_range: string;
}

const subjectIcons: Record<string, any> = {
  verbal_reasoning: PenTool,
  mathematics: Calculator,
  non_verbal_reasoning: Puzzle,
  english: BookOpen,
};

const subjectColors: Record<string, string> = {
  verbal_reasoning: "purple",
  mathematics: "green",
  non_verbal_reasoning: "blue",
  english: "amber",
};

export default function StrategiesPage() {
  const [strategies, setStrategies] = useState<Strategy[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedSubject, setSelectedSubject] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_BASE}/api/strategies`)
      .then((res) => res.json())
      .then((data) => {
        setStrategies(data.strategies || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error loading strategies:", err);
        setLoading(false);
      });
  }, []);

  const groupedStrategies = strategies.reduce((acc, strategy) => {
    if (!acc[strategy.subject]) {
      acc[strategy.subject] = [];
    }
    acc[strategy.subject].push(strategy);
    return acc;
  }, {} as Record<string, Strategy[]>);

  const subjects = Object.keys(groupedStrategies);

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
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center">
            <Lightbulb className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
              Strategy Guides
            </h1>
            <p className="text-slate-500 dark:text-slate-400">
              Learn how to approach each question type
            </p>
          </div>
        </div>
      </div>

      {/* Info Banner */}
      <div className="bg-gradient-to-r from-amber-50 to-orange-50 dark:from-amber-900/20 dark:to-orange-900/20 rounded-xl p-4 mb-6 border border-amber-200 dark:border-amber-800">
        <div className="flex items-start gap-3">
          <Target className="w-5 h-5 text-amber-600 mt-0.5" />
          <div>
            <p className="text-sm text-amber-800 dark:text-amber-200">
              <strong>Pro tip:</strong> Read the strategy guide BEFORE practicing each question type.
              Understanding the approach will help you solve questions faster and more accurately.
            </p>
          </div>
        </div>
      </div>

      {/* Subject Filter */}
      <div className="flex flex-wrap gap-2 mb-6">
        <button
          onClick={() => setSelectedSubject(null)}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            selectedSubject === null
              ? "bg-slate-900 text-white dark:bg-white dark:text-slate-900"
              : "bg-slate-100 text-slate-600 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300"
          }`}
        >
          All
        </button>
        {subjects.map((subject) => {
          const Icon = subjectIcons[subject] || BookOpen;
          return (
            <button
              key={subject}
              onClick={() => setSelectedSubject(subject)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 ${
                selectedSubject === subject
                  ? "bg-slate-900 text-white dark:bg-white dark:text-slate-900"
                  : "bg-slate-100 text-slate-600 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300"
              }`}
            >
              <Icon className="w-4 h-4" />
              {subject.replace("_", " ").replace(/\b\w/g, (l) => l.toUpperCase())}
            </button>
          );
        })}
      </div>

      {/* Strategy Cards */}
      <div className="space-y-6">
        {subjects
          .filter((subject) => !selectedSubject || subject === selectedSubject)
          .map((subject) => {
            const Icon = subjectIcons[subject] || BookOpen;
            const color = subjectColors[subject] || "slate";
            const subjectStrategies = groupedStrategies[subject];

            return (
              <div key={subject} className="space-y-3">
                <div className="flex items-center gap-2 text-sm font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                  <Icon className="w-4 h-4" />
                  {subject.replace("_", " ")}
                </div>

                <div className="grid gap-3">
                  {subjectStrategies.map((strategy) => (
                    <Link
                      key={strategy.question_type}
                      href={`/strategies/${strategy.question_type}`}
                      className="bg-white dark:bg-slate-800 rounded-xl p-4 border border-slate-200 dark:border-slate-700 hover:shadow-md hover:border-slate-300 dark:hover:border-slate-600 transition-all group"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <div className={`w-10 h-10 rounded-lg bg-${color}-100 dark:bg-${color}-900/30 flex items-center justify-center`}>
                            <Lightbulb className={`w-5 h-5 text-${color}-600 dark:text-${color}-400`} />
                          </div>
                          <div>
                            <h3 className="font-semibold text-slate-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                              {strategy.title}
                            </h3>
                            <div className="flex items-center gap-3 mt-1 text-xs text-slate-500">
                              {strategy.difficulty_range && (
                                <span className="flex items-center gap-1">
                                  <Target className="w-3 h-3" />
                                  Difficulty {strategy.difficulty_range}
                                </span>
                              )}
                              {strategy.is_free ? (
                                <span className="text-green-600 dark:text-green-400">Free</span>
                              ) : (
                                <span className="text-amber-600 dark:text-amber-400">Premium</span>
                              )}
                            </div>
                          </div>
                        </div>
                        <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors" />
                      </div>
                    </Link>
                  ))}
                </div>
              </div>
            );
          })}
      </div>

      {strategies.length === 0 && (
        <div className="text-center py-12 text-slate-500">
          <Lightbulb className="w-12 h-12 mx-auto mb-4 opacity-50" />
          <p>No strategy guides available yet.</p>
        </div>
      )}
    </div>
  );
}

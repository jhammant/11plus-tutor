"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
  Lightbulb,
  ArrowLeft,
  CheckCircle2,
  AlertTriangle,
  Clock,
  Target,
  ChevronRight,
  BookOpen,
} from "lucide-react";

const API_BASE = "http://localhost:8002";

interface WorkedExample {
  question: string;
  answer: string;
  walkthrough?: string;
  options?: string[];
}

interface Strategy {
  question_type: string;
  subject: string;
  title: string;
  what_is_it: string;
  approach: string[];
  common_mistakes: string[];
  time_tips: string[];
  worked_examples: WorkedExample[];
  typical_time_seconds: number;
  difficulty_range: string;
  is_free: boolean;
}

export default function StrategyDetailPage() {
  const params = useParams();
  const questionType = params.type as string;

  const [strategy, setStrategy] = useState<Strategy | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedExample, setExpandedExample] = useState<number | null>(0);

  useEffect(() => {
    if (!questionType) return;

    fetch(`${API_BASE}/api/strategies/${questionType}`)
      .then((res) => {
        if (!res.ok) throw new Error("Strategy not found");
        return res.json();
      })
      .then((data) => {
        setStrategy(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [questionType]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error || !strategy) {
    return (
      <div className="max-w-2xl mx-auto text-center py-12">
        <AlertTriangle className="w-12 h-12 mx-auto mb-4 text-amber-500" />
        <h2 className="text-xl font-bold mb-2">Strategy Not Found</h2>
        <p className="text-slate-500 mb-4">
          We couldn't find a strategy guide for "{questionType}".
        </p>
        <Link
          href="/strategies"
          className="text-blue-600 hover:text-blue-700 font-medium"
        >
          ← Back to all strategies
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto">
      {/* Back Link */}
      <Link
        href="/strategies"
        className="inline-flex items-center gap-2 text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 mb-6 text-sm"
      >
        <ArrowLeft className="w-4 h-4" />
        All Strategies
      </Link>

      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center">
            <Lightbulb className="w-7 h-7 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
              {strategy.title}
            </h1>
            <div className="flex items-center gap-3 text-sm text-slate-500">
              <span className="capitalize">{strategy.subject?.replace("_", " ")}</span>
              {strategy.difficulty_range && (
                <>
                  <span>•</span>
                  <span className="flex items-center gap-1">
                    <Target className="w-3 h-3" />
                    Difficulty {strategy.difficulty_range}
                  </span>
                </>
              )}
              {strategy.typical_time_seconds && (
                <>
                  <span>•</span>
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    ~{Math.round(strategy.typical_time_seconds / 60)} min
                  </span>
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* What Is It */}
      <section className="mb-8">
        <h2 className="text-lg font-bold text-slate-900 dark:text-white mb-3 flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-blue-600" />
          What is this question type?
        </h2>
        <div className="bg-blue-50 dark:bg-blue-900/20 rounded-xl p-5 border border-blue-200 dark:border-blue-800">
          <p className="text-slate-700 dark:text-slate-300 whitespace-pre-line">
            {strategy.what_is_it}
          </p>
        </div>
      </section>

      {/* Approach */}
      <section className="mb-8">
        <h2 className="text-lg font-bold text-slate-900 dark:text-white mb-3 flex items-center gap-2">
          <Target className="w-5 h-5 text-green-600" />
          Step-by-Step Approach
        </h2>
        <div className="bg-white dark:bg-slate-800 rounded-xl p-5 border border-slate-200 dark:border-slate-700">
          <ol className="space-y-3">
            {strategy.approach?.map((step, i) => (
              <li key={i} className="flex items-start gap-3">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 text-sm font-bold flex items-center justify-center">
                  {i + 1}
                </span>
                <span className="text-slate-700 dark:text-slate-300">{step}</span>
              </li>
            ))}
          </ol>
        </div>
      </section>

      {/* Common Mistakes */}
      {strategy.common_mistakes && strategy.common_mistakes.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-bold text-slate-900 dark:text-white mb-3 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-600" />
            Common Mistakes to Avoid
          </h2>
          <div className="bg-amber-50 dark:bg-amber-900/20 rounded-xl p-5 border border-amber-200 dark:border-amber-800">
            <ul className="space-y-2">
              {strategy.common_mistakes.map((mistake, i) => (
                <li key={i} className="flex items-start gap-2 text-slate-700 dark:text-slate-300">
                  <span className="text-amber-600">✗</span>
                  {mistake}
                </li>
              ))}
            </ul>
          </div>
        </section>
      )}

      {/* Time Tips */}
      {strategy.time_tips && strategy.time_tips.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-bold text-slate-900 dark:text-white mb-3 flex items-center gap-2">
            <Clock className="w-5 h-5 text-purple-600" />
            Time Management Tips
          </h2>
          <div className="bg-purple-50 dark:bg-purple-900/20 rounded-xl p-5 border border-purple-200 dark:border-purple-800">
            <ul className="space-y-2">
              {strategy.time_tips.map((tip, i) => (
                <li key={i} className="flex items-start gap-2 text-slate-700 dark:text-slate-300">
                  <span className="text-purple-600">⏱</span>
                  {tip}
                </li>
              ))}
            </ul>
          </div>
        </section>
      )}

      {/* Worked Examples */}
      {strategy.worked_examples && strategy.worked_examples.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-bold text-slate-900 dark:text-white mb-3 flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-600" />
            Worked Examples
          </h2>
          <div className="space-y-4">
            {strategy.worked_examples.map((example, i) => (
              <div
                key={i}
                className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden"
              >
                <button
                  onClick={() => setExpandedExample(expandedExample === i ? null : i)}
                  className="w-full px-5 py-4 text-left flex items-center justify-between hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors"
                >
                  <div>
                    <span className="text-xs font-medium text-slate-500 uppercase">
                      Example {i + 1}
                    </span>
                    <p className="text-slate-900 dark:text-white font-medium mt-1 whitespace-pre-line">
                      {example.question}
                    </p>
                  </div>
                  <ChevronRight
                    className={`w-5 h-5 text-slate-400 transition-transform ${
                      expandedExample === i ? "rotate-90" : ""
                    }`}
                  />
                </button>

                {expandedExample === i && (
                  <div className="px-5 pb-5 border-t border-slate-200 dark:border-slate-700">
                    {/* Options if present */}
                    {example.options && (
                      <div className="mt-4 space-y-2">
                        {example.options.map((opt, j) => (
                          <div
                            key={j}
                            className={`px-4 py-2 rounded-lg text-sm ${
                              opt === example.answer || opt.includes(example.answer)
                                ? "bg-emerald-100 dark:bg-emerald-900/30 text-emerald-800 dark:text-emerald-200 font-medium"
                                : "bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-400"
                            }`}
                          >
                            {String.fromCharCode(65 + j)}. {opt}
                            {(opt === example.answer || opt.includes(example.answer)) && " ✓"}
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Answer */}
                    <div className="mt-4 p-4 bg-emerald-50 dark:bg-emerald-900/20 rounded-lg border border-emerald-200 dark:border-emerald-800">
                      <p className="text-sm font-medium text-emerald-800 dark:text-emerald-200">
                        Answer: {example.answer}
                      </p>
                    </div>

                    {/* Walkthrough */}
                    {example.walkthrough && (
                      <div className="mt-4 p-4 bg-slate-50 dark:bg-slate-900/50 rounded-lg">
                        <p className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                          Step-by-step solution:
                        </p>
                        <p className="text-sm text-slate-600 dark:text-slate-400 whitespace-pre-line">
                          {example.walkthrough}
                        </p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Practice CTA */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-6 text-white">
        <h3 className="text-lg font-bold mb-2">Ready to Practice?</h3>
        <p className="text-blue-100 mb-4">
          Now that you understand the strategy, put it into practice with real questions.
        </p>
        <Link
          href={`/practice?type=${strategy.question_type}`}
          className="inline-flex items-center gap-2 bg-white text-blue-600 px-5 py-2 rounded-lg font-medium hover:bg-blue-50 transition-colors"
        >
          Practice {strategy.title}
          <ChevronRight className="w-4 h-4" />
        </Link>
      </div>
    </div>
  );
}

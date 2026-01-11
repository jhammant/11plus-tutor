"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
  BookOpen,
  ArrowLeft,
  CheckCircle2,
  AlertTriangle,
  Clock,
  Target,
  ChevronRight,
  Play,
  Lightbulb,
} from "lucide-react";

const API_BASE = "http://localhost:8002";

interface WorkedExample {
  question: string;
  answer: string;
  explanation?: string;
  walkthrough?: string;
}

interface Lesson {
  subject: string;
  topic: string;
  title: string;
  explanation: string;
  key_points: string[];
  worked_examples: WorkedExample[];
  tips?: string[];
  common_mistakes?: string[];
  is_free: boolean;
}

export default function LessonPage() {
  const params = useParams();
  const subject = params.subject as string;
  const topic = params.topic as string;

  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedExample, setExpandedExample] = useState<number | null>(0);

  useEffect(() => {
    if (!subject || !topic) return;

    fetch(`${API_BASE}/api/learn/${subject}/${topic}`)
      .then((res) => {
        if (!res.ok) throw new Error("Lesson not found");
        return res.json();
      })
      .then((data) => {
        setLesson(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [subject, topic]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error || !lesson) {
    return (
      <div className="max-w-2xl mx-auto text-center py-12">
        <AlertTriangle className="w-12 h-12 mx-auto mb-4 text-amber-500" />
        <h2 className="text-xl font-bold mb-2">Lesson Not Found</h2>
        <p className="text-slate-500 mb-4">
          We couldn't find a lesson for "{topic}".
        </p>
        <Link
          href="/learn"
          className="text-blue-600 hover:text-blue-700 font-medium"
        >
          ← Back to Learn
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto">
      {/* Back Link */}
      <Link
        href="/learn"
        className="inline-flex items-center gap-2 text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 mb-6 text-sm"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Learn
      </Link>

      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center">
            <BookOpen className="w-7 h-7 text-white" />
          </div>
          <div>
            <p className="text-sm text-slate-500 capitalize">
              {subject?.replace("_", " ")}
            </p>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
              {lesson.title}
            </h1>
          </div>
        </div>
      </div>

      {/* Main Explanation */}
      <section className="mb-8">
        <div className="bg-blue-50 dark:bg-blue-900/20 rounded-xl p-6 border border-blue-200 dark:border-blue-800">
          <h2 className="text-lg font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-blue-600" />
            Understanding {lesson.title}
          </h2>
          <div className="prose prose-slate dark:prose-invert max-w-none">
            <p className="text-slate-700 dark:text-slate-300 whitespace-pre-line leading-relaxed">
              {lesson.explanation}
            </p>
          </div>
        </div>
      </section>

      {/* Key Points / Approach */}
      {lesson.key_points && lesson.key_points.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-bold text-slate-900 dark:text-white mb-3 flex items-center gap-2">
            <Target className="w-5 h-5 text-green-600" />
            Key Steps
          </h2>
          <div className="bg-white dark:bg-slate-800 rounded-xl p-5 border border-slate-200 dark:border-slate-700">
            <ol className="space-y-3">
              {lesson.key_points.map((point, i) => (
                <li key={i} className="flex items-start gap-3">
                  <span className="flex-shrink-0 w-6 h-6 rounded-full bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 text-sm font-bold flex items-center justify-center">
                    {i + 1}
                  </span>
                  <span className="text-slate-700 dark:text-slate-300">{point}</span>
                </li>
              ))}
            </ol>
          </div>
        </section>
      )}

      {/* Common Mistakes */}
      {lesson.common_mistakes && lesson.common_mistakes.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-bold text-slate-900 dark:text-white mb-3 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-600" />
            Watch Out For
          </h2>
          <div className="bg-amber-50 dark:bg-amber-900/20 rounded-xl p-5 border border-amber-200 dark:border-amber-800">
            <ul className="space-y-2">
              {lesson.common_mistakes.map((mistake, i) => (
                <li key={i} className="flex items-start gap-2 text-slate-700 dark:text-slate-300">
                  <span className="text-amber-600">✗</span>
                  {mistake}
                </li>
              ))}
            </ul>
          </div>
        </section>
      )}

      {/* Worked Examples */}
      {lesson.worked_examples && lesson.worked_examples.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-bold text-slate-900 dark:text-white mb-3 flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-600" />
            Worked Examples
          </h2>
          <div className="space-y-4">
            {lesson.worked_examples.map((example, i) => (
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
                    <p className="text-slate-900 dark:text-white font-medium mt-1">
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
                    {/* Answer */}
                    <div className="mt-4 p-4 bg-emerald-50 dark:bg-emerald-900/20 rounded-lg border border-emerald-200 dark:border-emerald-800">
                      <p className="text-sm font-medium text-emerald-800 dark:text-emerald-200">
                        Answer: {example.answer}
                      </p>
                    </div>

                    {/* Explanation/Walkthrough */}
                    {(example.explanation || example.walkthrough) && (
                      <div className="mt-4 p-4 bg-slate-50 dark:bg-slate-900/50 rounded-lg">
                        <p className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                          Solution:
                        </p>
                        <p className="text-sm text-slate-600 dark:text-slate-400 whitespace-pre-line">
                          {example.explanation || example.walkthrough}
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
          Now that you understand {lesson.title.toLowerCase()}, put it into practice!
        </p>
        <Link
          href={`/practice?subject=${subject}&type=${topic}`}
          className="inline-flex items-center gap-2 bg-white text-blue-600 px-5 py-2 rounded-lg font-medium hover:bg-blue-50 transition-colors"
        >
          <Play className="w-4 h-4" />
          Practice Now
        </Link>
      </div>
    </div>
  );
}

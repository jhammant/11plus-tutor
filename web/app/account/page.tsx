"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import {
  User,
  BarChart3,
  ArrowLeft,
  Sparkles,
  BookOpen,
  Target,
  Github,
} from "lucide-react";

interface Stats {
  total_attempted: number;
  total_correct: number;
  accuracy: number;
}

export default function AccountPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [studentId, setStudentId] = useState<string>("");

  useEffect(() => {
    // Get or create student ID from localStorage
    let id = localStorage.getItem("elevenplustutor_student_id");
    if (!id) {
      id = `student_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem("elevenplustutor_student_id", id);
    }
    setStudentId(id);

    // Fetch progress stats
    fetch(`http://localhost:8002/api/progress/${id}`)
      .then((res) => res.json())
      .then((data) => setStats(data))
      .catch((err) => console.error("Failed to fetch stats:", err));
  }, []);

  return (
    <div className="max-w-4xl mx-auto px-6 py-8">
      <Link
        href="/"
        className="inline-flex items-center gap-2 text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200 mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Dashboard
      </Link>

      <h1 className="text-3xl font-bold text-slate-900 dark:text-white mb-8">
        Your Profile
      </h1>

      <div className="grid gap-6">
        {/* Profile Card */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 border border-slate-200 dark:border-slate-700">
          <div className="flex items-center gap-4 mb-6">
            <div className="w-16 h-16 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white text-2xl font-bold">
              <User className="w-8 h-8" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-slate-900 dark:text-white">
                Student
              </h2>
              <p className="text-slate-500 dark:text-slate-400 text-sm font-mono">
                ID: {studentId.slice(0, 12)}...
              </p>
            </div>
            <div className="ml-auto flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-emerald-500 to-teal-500 text-white rounded-full">
              <Sparkles className="w-4 h-4" />
              <span className="font-semibold">Free Forever</span>
            </div>
          </div>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Your progress is saved locally on this device.
          </p>
        </div>

        {/* Stats Card */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 border border-slate-200 dark:border-slate-700">
          <div className="flex items-center gap-3 mb-6">
            <BarChart3 className="w-6 h-6 text-purple-500" />
            <h2 className="text-xl font-bold text-slate-900 dark:text-white">
              Your Progress
            </h2>
          </div>

          {stats ? (
            <div className="grid grid-cols-3 gap-4">
              <div className="text-center p-4 bg-slate-50 dark:bg-slate-700/50 rounded-xl">
                <div className="text-3xl font-bold text-slate-900 dark:text-white">
                  {stats.total_attempted}
                </div>
                <div className="text-sm text-slate-500 dark:text-slate-400">
                  Questions Attempted
                </div>
              </div>
              <div className="text-center p-4 bg-slate-50 dark:bg-slate-700/50 rounded-xl">
                <div className="text-3xl font-bold text-emerald-600">
                  {stats.total_correct}
                </div>
                <div className="text-sm text-slate-500 dark:text-slate-400">
                  Correct Answers
                </div>
              </div>
              <div className="text-center p-4 bg-slate-50 dark:bg-slate-700/50 rounded-xl">
                <div className="text-3xl font-bold text-blue-600">
                  {stats.accuracy}%
                </div>
                <div className="text-sm text-slate-500 dark:text-slate-400">
                  Accuracy
                </div>
              </div>
            </div>
          ) : (
            <p className="text-slate-500 dark:text-slate-400">
              Start practicing to see your progress!
            </p>
          )}
        </div>

        {/* Open Source Info */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-6 text-white">
          <div className="flex items-center gap-3 mb-4">
            <Github className="w-6 h-6" />
            <h2 className="text-xl font-bold">Open Source & Free</h2>
          </div>
          <p className="text-blue-100 mb-4">
            11+ Tutor is completely free and open source. No accounts, no
            subscriptions, no limits. Your data stays on your device.
          </p>
          <div className="flex gap-4">
            <a
              href="https://github.com/yourusername/11plus-tutor"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg transition-colors"
            >
              <Github className="w-4 h-4" />
              View on GitHub
            </a>
          </div>
        </div>

        {/* Quick Links */}
        <div className="grid grid-cols-2 gap-4">
          <Link
            href="/learn"
            className="flex items-center gap-3 p-4 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 hover:border-blue-500 transition-colors"
          >
            <BookOpen className="w-6 h-6 text-blue-500" />
            <div>
              <h3 className="font-semibold text-slate-900 dark:text-white">
                Topic Lessons
              </h3>
              <p className="text-sm text-slate-500">Learn the concepts</p>
            </div>
          </Link>
          <Link
            href="/practice"
            className="flex items-center gap-3 p-4 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 hover:border-blue-500 transition-colors"
          >
            <Target className="w-6 h-6 text-purple-500" />
            <div>
              <h3 className="font-semibold text-slate-900 dark:text-white">
                Practice Questions
              </h3>
              <p className="text-sm text-slate-500">Test your skills</p>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
}

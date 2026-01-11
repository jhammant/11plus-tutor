"use client";

import { useState } from "react";
import Link from "next/link";
import {
  BookOpen,
  Users,
  GraduationCap,
  Play,
  Timer,
  Keyboard,
  Lightbulb,
  Target,
  Trophy,
  Flame,
  CheckCircle2,
  ArrowRight,
  Sparkles,
  Heart,
  Star,
  Clock,
  Calendar,
  Brain,
  Puzzle,
  Calculator,
  PenTool,
  ChevronDown,
  ChevronUp,
} from "lucide-react";

type Tab = "parents" | "kids";

export default function GettingStartedPage() {
  const [activeTab, setActiveTab] = useState<Tab>("parents");
  const [expandedFaq, setExpandedFaq] = useState<number | null>(null);

  return (
    <div className="max-w-4xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 dark:bg-blue-900/30 rounded-full text-blue-600 dark:text-blue-400 text-sm font-medium mb-4">
          <Sparkles className="w-4 h-4" />
          Free & Open Source
        </div>
        <h1 className="text-4xl font-bold text-slate-900 dark:text-white mb-4">
          Welcome to 11+ Tutor
        </h1>
        <p className="text-xl text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
          Free practice for grammar school entrance exams. No subscriptions, no hidden costs.
          Just quality practice to help every child succeed.
        </p>
      </div>

      {/* Tab Selector */}
      <div className="flex justify-center mb-8">
        <div className="bg-slate-100 dark:bg-slate-800 rounded-2xl p-1.5 inline-flex">
          <button
            onClick={() => setActiveTab("parents")}
            className={`px-6 py-3 rounded-xl font-medium transition-all flex items-center gap-2 ${
              activeTab === "parents"
                ? "bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm"
                : "text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white"
            }`}
          >
            <Users className="w-5 h-5" />
            For Parents
          </button>
          <button
            onClick={() => setActiveTab("kids")}
            className={`px-6 py-3 rounded-xl font-medium transition-all flex items-center gap-2 ${
              activeTab === "kids"
                ? "bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm"
                : "text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white"
            }`}
          >
            <GraduationCap className="w-5 h-5" />
            For Kids
          </button>
        </div>
      </div>

      {/* Parent Guide */}
      {activeTab === "parents" && (
        <div className="space-y-8">
          {/* Quick Start for Parents */}
          <div className="bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl p-8 text-white">
            <h2 className="text-2xl font-bold mb-4">Quick Start Guide</h2>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="bg-white/10 rounded-xl p-5">
                <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center mb-3">
                  <span className="text-xl font-bold">1</span>
                </div>
                <h3 className="font-semibold mb-2">Start Practicing</h3>
                <p className="text-sm opacity-90">
                  Click "Practice Questions" on the home page. Your child can start immediately - no account needed.
                </p>
              </div>
              <div className="bg-white/10 rounded-xl p-5">
                <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center mb-3">
                  <span className="text-xl font-bold">2</span>
                </div>
                <h3 className="font-semibold mb-2">Focus on Weak Areas</h3>
                <p className="text-sm opacity-90">
                  Use the subject filters to practice specific topics. Check Progress to see where they need more work.
                </p>
              </div>
              <div className="bg-white/10 rounded-xl p-5">
                <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center mb-3">
                  <span className="text-xl font-bold">3</span>
                </div>
                <h3 className="font-semibold mb-2">Build Consistency</h3>
                <p className="text-sm opacity-90">
                  Aim for 20 questions daily. The streak tracker helps motivate regular practice.
                </p>
              </div>
            </div>
          </div>

          {/* What's Included */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6">
            <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-6">What's Included (All Free)</h2>
            <div className="grid md:grid-cols-2 gap-4">
              {[
                { icon: PenTool, title: "Verbal Reasoning", desc: "1,000+ questions: synonyms, antonyms, analogies, codes, sequences" },
                { icon: Puzzle, title: "Non-Verbal Reasoning", desc: "SVG-based shape questions: sequences, odd one out, analogies" },
                { icon: Calculator, title: "Mathematics", desc: "Arithmetic, fractions, number sequences - KS2 aligned" },
                { icon: BookOpen, title: "English", desc: "Reading comprehension, spelling, grammar" },
                { icon: Timer, title: "Exam Simulation", desc: "Per-question timer to practice pacing (aim for under 50 seconds)" },
                { icon: Lightbulb, title: "Strategy Guides", desc: "Step-by-step techniques for each question type" },
                { icon: Target, title: "Progress Tracking", desc: "See accuracy by subject and question type" },
                { icon: Keyboard, title: "Keyboard Shortcuts", desc: "A-E to select, Enter to submit - faster practice" },
              ].map((item, i) => {
                const Icon = item.icon;
                return (
                  <div key={i} className="flex gap-4 p-3 rounded-xl bg-slate-50 dark:bg-slate-700/50">
                    <Icon className="w-6 h-6 text-blue-500 flex-shrink-0 mt-0.5" />
                    <div>
                      <h3 className="font-semibold text-slate-900 dark:text-white">{item.title}</h3>
                      <p className="text-sm text-slate-600 dark:text-slate-400">{item.desc}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Recommended Schedule */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6">
            <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
              <Calendar className="w-6 h-6 text-blue-500" />
              Recommended Practice Schedule
            </h2>
            <div className="space-y-4">
              <div className="p-4 bg-emerald-50 dark:bg-emerald-900/20 rounded-xl border border-emerald-200 dark:border-emerald-800">
                <h3 className="font-semibold text-emerald-800 dark:text-emerald-300 mb-2">Daily (15-20 minutes)</h3>
                <ul className="text-sm text-emerald-700 dark:text-emerald-400 space-y-1">
                  <li>• 20 mixed questions OR focused practice on one weak area</li>
                  <li>• Review incorrect answers and explanations</li>
                  <li>• Use the Strategy Guide for question types they struggle with</li>
                </ul>
              </div>
              <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-xl border border-blue-200 dark:border-blue-800">
                <h3 className="font-semibold text-blue-800 dark:text-blue-300 mb-2">Weekly (30-45 minutes)</h3>
                <ul className="text-sm text-blue-700 dark:text-blue-400 space-y-1">
                  <li>• One timed Mock Exam to simulate test conditions</li>
                  <li>• Review the Progress page to identify weak areas</li>
                  <li>• Focus next week's practice on lowest-scoring topics</li>
                </ul>
              </div>
              <div className="p-4 bg-amber-50 dark:bg-amber-900/20 rounded-xl border border-amber-200 dark:border-amber-800">
                <h3 className="font-semibold text-amber-800 dark:text-amber-300 mb-2">Tips for Parents</h3>
                <ul className="text-sm text-amber-700 dark:text-amber-400 space-y-1">
                  <li>• Sit with them initially to explain how to use hints and strategies</li>
                  <li>• Praise effort and improvement, not just correct answers</li>
                  <li>• Take breaks - tired practice is unproductive practice</li>
                  <li>• Consistency beats intensity: 20 mins daily beats 2 hours once a week</li>
                </ul>
              </div>
            </div>
          </div>

          {/* FAQ */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6">
            <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-4">Frequently Asked Questions</h2>
            <div className="space-y-2">
              {[
                {
                  q: "Is this really free? What's the catch?",
                  a: "Yes, completely free and open source (MIT license). There's no catch - I built this for my own child and wanted to help other families. The code is on GitHub for anyone to inspect."
                },
                {
                  q: "Are the questions accurate?",
                  a: "All questions are programmatically verified or validated against curated word lists. We have 57 automated tests that check every question type. If you find an error, report it and we'll fix it same day."
                },
                {
                  q: "Does it work for GL and CEM exams?",
                  a: "The current questions are primarily GL-style. CEM-style questions are on our roadmap. The verbal reasoning and maths content works for both exam types."
                },
                {
                  q: "Is my child's data stored somewhere?",
                  a: "Progress is stored locally in your browser only. Nothing is sent to any server. Your data stays on your computer."
                },
                {
                  q: "How do printable worksheets work?",
                  a: "Run the worksheet generator script to create HTML worksheets you can print. Great for offline practice or car journeys!"
                },
                {
                  q: "Do I need to install AI software?",
                  a: "No! All 1,364 questions work without any AI. The AI tutor is optional - only needed if you want 'Explain this answer' features. See README.md for easy setup options if you want AI (LM Studio, Ollama, or cloud services like OpenAI/Groq)."
                },
                {
                  q: "Will this run on my old laptop?",
                  a: "Yes! The basic app is lightweight and runs on any computer. You only need a powerful machine (8GB+ RAM) if you want to run a local AI model. Alternatively, use a cloud AI service which works on any device."
                },
              ].map((faq, i) => (
                <div key={i} className="border border-slate-200 dark:border-slate-700 rounded-xl overflow-hidden">
                  <button
                    onClick={() => setExpandedFaq(expandedFaq === i ? null : i)}
                    className="w-full p-4 text-left flex items-center justify-between hover:bg-slate-50 dark:hover:bg-slate-700/50"
                  >
                    <span className="font-medium text-slate-900 dark:text-white">{faq.q}</span>
                    {expandedFaq === i ? (
                      <ChevronUp className="w-5 h-5 text-slate-500" />
                    ) : (
                      <ChevronDown className="w-5 h-5 text-slate-500" />
                    )}
                  </button>
                  {expandedFaq === i && (
                    <div className="px-4 pb-4 text-slate-600 dark:text-slate-400">
                      {faq.a}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* CTA */}
          <div className="text-center">
            <Link
              href="/practice"
              className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all"
            >
              <Play className="w-5 h-5" />
              Start Practicing Now
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      )}

      {/* Kids Guide */}
      {activeTab === "kids" && (
        <div className="space-y-8">
          {/* Fun Welcome */}
          <div className="bg-gradient-to-br from-purple-500 via-pink-500 to-orange-500 rounded-2xl p-8 text-white text-center">
            <div className="text-6xl mb-4">🎯</div>
            <h2 className="text-3xl font-bold mb-3">Ready to Become an 11+ Champion?</h2>
            <p className="text-xl opacity-90 max-w-xl mx-auto">
              This is YOUR training ground! Practice questions, learn tricks, and get ready to ace your exam!
            </p>
          </div>

          {/* How It Works - Kid Friendly */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6">
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-6 text-center">
              How to Use 11+ Tutor 🚀
            </h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-blue-50 dark:bg-blue-900/20 rounded-xl p-5 border-2 border-blue-200 dark:border-blue-800">
                <div className="text-4xl mb-3">1️⃣</div>
                <h3 className="font-bold text-lg text-slate-900 dark:text-white mb-2">Pick a Subject</h3>
                <p className="text-slate-600 dark:text-slate-400">
                  Choose what you want to practice: Words, Shapes, Maths, or Reading. Or just click "Practice" for a mix!
                </p>
              </div>
              <div className="bg-green-50 dark:bg-green-900/20 rounded-xl p-5 border-2 border-green-200 dark:border-green-800">
                <div className="text-4xl mb-3">2️⃣</div>
                <h3 className="font-bold text-lg text-slate-900 dark:text-white mb-2">Answer Questions</h3>
                <p className="text-slate-600 dark:text-slate-400">
                  Read carefully, pick your answer (A, B, C, D, or E), then click Submit. You can use your keyboard too!
                </p>
              </div>
              <div className="bg-amber-50 dark:bg-amber-900/20 rounded-xl p-5 border-2 border-amber-200 dark:border-amber-800">
                <div className="text-4xl mb-3">3️⃣</div>
                <h3 className="font-bold text-lg text-slate-900 dark:text-white mb-2">Learn from Mistakes</h3>
                <p className="text-slate-600 dark:text-slate-400">
                  Got it wrong? No problem! Read the explanation to understand why. That's how you get better!
                </p>
              </div>
              <div className="bg-purple-50 dark:bg-purple-900/20 rounded-xl p-5 border-2 border-purple-200 dark:border-purple-800">
                <div className="text-4xl mb-3">4️⃣</div>
                <h3 className="font-bold text-lg text-slate-900 dark:text-white mb-2">Build Your Streak!</h3>
                <p className="text-slate-600 dark:text-slate-400">
                  Get questions right in a row to build a streak. Can you get to 10? 20? How high can you go? 🔥
                </p>
              </div>
            </div>
          </div>

          {/* Secret Shortcuts */}
          <div className="bg-slate-900 dark:bg-slate-950 rounded-2xl p-6 text-white">
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
              <Keyboard className="w-7 h-7 text-yellow-400" />
              Secret Keyboard Shortcuts! 🎮
            </h2>
            <p className="text-slate-300 mb-4">Use these to answer super fast - just like a pro!</p>
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-slate-800 rounded-xl p-4 text-center">
                <div className="text-3xl font-mono font-bold text-yellow-400 mb-2">A B C D E</div>
                <p className="text-sm text-slate-400">Pick your answer</p>
              </div>
              <div className="bg-slate-800 rounded-xl p-4 text-center">
                <div className="text-3xl font-mono font-bold text-green-400 mb-2">ENTER</div>
                <p className="text-sm text-slate-400">Submit & Next</p>
              </div>
              <div className="bg-slate-800 rounded-xl p-4 text-center">
                <div className="text-3xl font-mono font-bold text-blue-400 mb-2">H</div>
                <p className="text-sm text-slate-400">Get a Hint!</p>
              </div>
            </div>
          </div>

          {/* The 4 Subjects */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6">
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-6 text-center">
              The 4 Things You'll Practice 📚
            </h2>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="bg-purple-100 dark:bg-purple-900/30 rounded-xl p-5">
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-12 h-12 bg-purple-500 rounded-xl flex items-center justify-center">
                    <PenTool className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="font-bold text-lg text-slate-900 dark:text-white">Verbal Reasoning</h3>
                </div>
                <p className="text-slate-600 dark:text-slate-400 text-sm mb-3">Word puzzles! Find matching words, crack codes, spot patterns in letters.</p>
                <div className="flex flex-wrap gap-1">
                  <span className="px-2 py-1 bg-purple-200 dark:bg-purple-800 rounded text-xs">Synonyms</span>
                  <span className="px-2 py-1 bg-purple-200 dark:bg-purple-800 rounded text-xs">Antonyms</span>
                  <span className="px-2 py-1 bg-purple-200 dark:bg-purple-800 rounded text-xs">Code Words</span>
                </div>
              </div>
              <div className="bg-blue-100 dark:bg-blue-900/30 rounded-xl p-5">
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center">
                    <Puzzle className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="font-bold text-lg text-slate-900 dark:text-white">Non-Verbal Reasoning</h3>
                </div>
                <p className="text-slate-600 dark:text-slate-400 text-sm mb-3">Shape puzzles! Find patterns, spot the odd one out, complete sequences.</p>
                <div className="flex flex-wrap gap-1">
                  <span className="px-2 py-1 bg-blue-200 dark:bg-blue-800 rounded text-xs">Sequences</span>
                  <span className="px-2 py-1 bg-blue-200 dark:bg-blue-800 rounded text-xs">Odd One Out</span>
                  <span className="px-2 py-1 bg-blue-200 dark:bg-blue-800 rounded text-xs">Analogies</span>
                </div>
              </div>
              <div className="bg-green-100 dark:bg-green-900/30 rounded-xl p-5">
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center">
                    <Calculator className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="font-bold text-lg text-slate-900 dark:text-white">Mathematics</h3>
                </div>
                <p className="text-slate-600 dark:text-slate-400 text-sm mb-3">Number challenges! Calculate, find patterns, work with fractions.</p>
                <div className="flex flex-wrap gap-1">
                  <span className="px-2 py-1 bg-green-200 dark:bg-green-800 rounded text-xs">Arithmetic</span>
                  <span className="px-2 py-1 bg-green-200 dark:bg-green-800 rounded text-xs">Fractions</span>
                  <span className="px-2 py-1 bg-green-200 dark:bg-green-800 rounded text-xs">Sequences</span>
                </div>
              </div>
              <div className="bg-amber-100 dark:bg-amber-900/30 rounded-xl p-5">
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-12 h-12 bg-amber-500 rounded-xl flex items-center justify-center">
                    <BookOpen className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="font-bold text-lg text-slate-900 dark:text-white">English</h3>
                </div>
                <p className="text-slate-600 dark:text-slate-400 text-sm mb-3">Reading and writing! Understand stories, spell correctly, use good grammar.</p>
                <div className="flex flex-wrap gap-1">
                  <span className="px-2 py-1 bg-amber-200 dark:bg-amber-800 rounded text-xs">Comprehension</span>
                  <span className="px-2 py-1 bg-amber-200 dark:bg-amber-800 rounded text-xs">Spelling</span>
                  <span className="px-2 py-1 bg-amber-200 dark:bg-amber-800 rounded text-xs">Grammar</span>
                </div>
              </div>
            </div>
          </div>

          {/* Tips for Success */}
          <div className="bg-gradient-to-br from-emerald-500 to-teal-600 rounded-2xl p-6 text-white">
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
              <Star className="w-7 h-7 text-yellow-300" />
              Top Tips for Success!
            </h2>
            <div className="grid md:grid-cols-2 gap-4">
              {[
                { emoji: "⏱️", tip: "Watch the timer - aim to answer in under 50 seconds" },
                { emoji: "💡", tip: "Press H for hints when you're stuck" },
                { emoji: "📖", tip: "Read the question TWICE before answering" },
                { emoji: "🔥", tip: "Practice every day to build your streak" },
                { emoji: "🎯", tip: "Focus on subjects you find hardest" },
                { emoji: "😌", tip: "Take breaks when tired - fresh brain = better answers!" },
              ].map((item, i) => (
                <div key={i} className="flex items-center gap-3 bg-white/10 rounded-lg p-3">
                  <span className="text-2xl">{item.emoji}</span>
                  <span>{item.tip}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Big Start Button */}
          <div className="text-center">
            <Link
              href="/practice"
              className="inline-flex items-center gap-3 px-10 py-5 bg-gradient-to-r from-purple-600 via-pink-600 to-orange-500 text-white text-xl font-bold rounded-2xl shadow-lg hover:shadow-xl transition-all hover:scale-105"
            >
              <Play className="w-7 h-7" />
              Let's Go! Start Practicing!
              <Sparkles className="w-7 h-7" />
            </Link>
            <p className="mt-4 text-slate-500 dark:text-slate-400">
              You've got this! 💪
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

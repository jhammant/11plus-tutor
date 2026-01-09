"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  BookOpen,
  PenTool,
  Calculator,
  Settings,
  GraduationCap,
  Trophy,
  Target,
  Puzzle,
  BarChart3,
  Clock,
} from "lucide-react";

export default function Sidebar() {
  const pathname = usePathname();

  const navGroups = [
    {
      name: "Practice",
      items: [
        { name: "Dashboard", href: "/", icon: LayoutDashboard },
        { name: "Practice Questions", href: "/practice", icon: Target },
      ],
    },
    {
      name: "Subjects",
      items: [
        { name: "Verbal Reasoning", href: "/practice?subject=verbal_reasoning", icon: PenTool },
        { name: "Non-Verbal", href: "/practice?subject=non_verbal_reasoning", icon: Puzzle },
        { name: "Mathematics", href: "/practice?subject=mathematics", icon: Calculator },
        { name: "English", href: "/practice?subject=english", icon: BookOpen },
      ],
    },
    {
      name: "Progress",
      items: [
        { name: "My Progress", href: "/progress", icon: BarChart3 },
        { name: "Mock Exams", href: "/mock", icon: Clock },
        { name: "Achievements", href: "/achievements", icon: Trophy },
      ],
    },
  ];

  return (
    <div className="w-64 bg-slate-50/50 dark:bg-slate-800/50 h-full border-r border-slate-200 dark:border-slate-700 flex flex-col backdrop-blur-xl transition-colors duration-200">
      {/* Header */}
      <div className="p-6 border-b border-slate-100 dark:border-slate-700">
        <div className="flex flex-col gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
              <GraduationCap className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="font-bold text-slate-900 dark:text-slate-100 tracking-tight text-lg">
                11+ Tutor
              </h1>
              <p className="text-[10px] text-slate-500 dark:text-slate-400">
                Grammar School Prep
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto p-4 space-y-6">
        {navGroups.map((group, idx) => (
          <div key={idx}>
            {group.name && (
              <div className="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider px-4 mb-2">
                {group.name}
              </div>
            )}
            <div className="space-y-0.5">
              {group.items.map((item) => {
                const isActive = pathname === item.href ||
                  (item.href.includes('?') && pathname === item.href.split('?')[0]);
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`group flex items-center gap-3 px-4 py-2 rounded-lg transition-all duration-200 ease-in-out border ${
                      isActive
                        ? "bg-white dark:bg-slate-700 text-blue-600 dark:text-blue-400 shadow-sm border-slate-100 dark:border-slate-600"
                        : "text-slate-600 dark:text-slate-300 hover:bg-white dark:hover:bg-slate-700 hover:text-blue-600 dark:hover:text-blue-400 hover:shadow-sm border-transparent hover:border-slate-100 dark:hover:border-slate-600"
                    }`}
                  >
                    <item.icon
                      className={`w-4 h-4 transition-colors ${
                        isActive
                          ? "text-blue-500 dark:text-blue-400"
                          : "text-slate-400 dark:text-slate-500 group-hover:text-blue-500 dark:group-hover:text-blue-400"
                      }`}
                    />
                    <span className="font-medium text-sm">{item.name}</span>
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-slate-100 dark:border-slate-700 space-y-2 bg-slate-50/30 dark:bg-slate-800/30">
        {/* Exam Info */}
        <div className="px-4 py-3 bg-gradient-to-r from-purple-500/10 to-blue-500/10 rounded-lg border border-purple-200/50 dark:border-purple-800/50">
          <div className="text-xs font-semibold text-purple-700 dark:text-purple-300 mb-1">
            GL Assessment Format
          </div>
          <div className="text-[10px] text-slate-600 dark:text-slate-400">
            Prepare for grammar school entrance
          </div>
        </div>

        {/* Settings */}
        <Link
          href="/settings"
          className={`w-full flex items-center gap-3 px-4 py-2 rounded-lg transition-all text-sm ${
            pathname === "/settings"
              ? "bg-white dark:bg-slate-700 text-blue-600 dark:text-blue-400 shadow-sm border border-slate-100 dark:border-slate-600"
              : "text-slate-600 dark:text-slate-300 hover:bg-white dark:hover:bg-slate-700 hover:text-slate-900 dark:hover:text-slate-100"
          }`}
        >
          <Settings
            className={`w-4 h-4 ${pathname === "/settings" ? "text-blue-500 dark:text-blue-400" : "text-slate-400 dark:text-slate-500"}`}
          />
          <span>Settings</span>
        </Link>
      </div>
    </div>
  );
}

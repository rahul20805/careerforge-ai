"use client";

import Link from "next/link";
import { useState } from "react";

export default function Opportunities() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleParse = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    // Simulate API call to FastAPI backend
    setTimeout(() => setLoading(false), 1500);
  };

  return (
    <main className="min-h-screen bg-zinc-50 dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100 p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="flex justify-between items-end border-b border-zinc-200 dark:border-zinc-800 pb-4">
          <div>
            <h1 className="text-4xl font-bold tracking-tight">Discover Opportunities</h1>
            <p className="text-zinc-500 mt-1">Parse Job Descriptions via URL and get AI matching scores.</p>
          </div>
          <Link href="/dashboard" className="text-sm font-medium hover:underline text-blue-600 dark:text-blue-400">
            &larr; Dashboard
          </Link>
        </header>

        {/* Input Form */}
        <section className="bg-white dark:bg-zinc-900 p-6 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-sm">
          <form onSubmit={handleParse} className="flex gap-4">
            <input 
              type="url"
              required
              placeholder="Paste LinkedIn or Company Career page URL..."
              className="flex-1 px-4 py-3 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-transparent focus:ring-2 focus:ring-blue-500 outline-none"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
            <button 
              type="submit"
              disabled={loading}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-medium rounded-lg transition-colors"
            >
              {loading ? "Parsing..." : "Extract JD"}
            </button>
          </form>
        </section>

        {/* Mock Results */}
        {!loading && url && (
          <div className="p-6 rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 shadow-sm animate-in fade-in slide-in-from-bottom-4 duration-500">
            <h3 className="text-xl font-semibold mb-2">Parsed Opportunity</h3>
            <p className="text-zinc-500 mb-6">Matches your profile with an 85% ATS fit.</p>
            
            <div className="space-y-4">
              <div className="p-4 bg-zinc-50 dark:bg-zinc-800 rounded-lg">
                <span className="text-xs font-semibold uppercase tracking-wider text-zinc-500">Role</span>
                <p className="font-medium mt-1">Senior Frontend Engineer</p>
              </div>
              <div className="p-4 bg-zinc-50 dark:bg-zinc-800 rounded-lg">
                <span className="text-xs font-semibold uppercase tracking-wider text-zinc-500">Required Skills</span>
                <div className="flex gap-2 mt-2 flex-wrap">
                  {["React", "TypeScript", "Next.js", "GraphQL"].map(skill => (
                    <span key={skill} className="px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded text-sm font-medium">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            </div>
            
            <div className="mt-6 pt-6 border-t border-zinc-200 dark:border-zinc-800 flex justify-end">
              <Link href="/resumes">
                <button className="px-6 py-2 bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 font-medium rounded-lg hover:opacity-90 transition-opacity">
                  Generate Resume for this Role &rarr;
                </button>
              </Link>
            </div>
          </div>
        )}

      </div>
    </main>
  );
}

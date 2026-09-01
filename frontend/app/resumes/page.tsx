"use client";

import Link from "next/link";
import { useState } from "react";

export default function Resumes() {
  const [loading, setLoading] = useState(false);
  const [generated, setGenerated] = useState(false);

  const handleGenerate = () => {
    setLoading(true);
    // Simulate FastAPI backend generation (PDF/DOCX)
    setTimeout(() => {
      setLoading(false);
      setGenerated(true);
    }, 2500);
  };

  return (
    <main className="min-h-screen bg-zinc-50 dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100 p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="flex justify-between items-end border-b border-zinc-200 dark:border-zinc-800 pb-4">
          <div>
            <h1 className="text-4xl font-bold tracking-tight">AI Resume Generator</h1>
            <p className="text-zinc-500 mt-1">Truth-Verified Document Generation tailored to ATS requirements.</p>
          </div>
          <Link href="/dashboard" className="text-sm font-medium hover:underline text-blue-600 dark:text-blue-400">
            &larr; Dashboard
          </Link>
        </header>

        {/* Builder UI */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          
          <section className="space-y-6">
            <div className="p-6 bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-sm">
              <h2 className="font-semibold text-lg mb-4">Configuration</h2>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-zinc-500 mb-1">Target Opportunity</label>
                  <select className="w-full p-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-transparent outline-none">
                    <option>Senior Frontend Engineer - Google</option>
                    <option>Backend Engineer - Stripe</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-zinc-500 mb-1">Template Style</label>
                  <select className="w-full p-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-transparent outline-none">
                    <option>Modern ATS (Standard)</option>
                    <option>Academic CV</option>
                  </select>
                </div>
              </div>

              <button 
                onClick={handleGenerate}
                disabled={loading}
                className="w-full mt-6 px-4 py-3 bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 font-medium rounded-lg hover:opacity-90 disabled:opacity-50 transition-opacity"
              >
                {loading ? "Compiling Document..." : "Generate Truth-Verified Resume"}
              </button>
            </div>
          </section>

          <section>
            <div className="p-6 h-full min-h-[400px] bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-sm flex flex-col items-center justify-center text-center">
              {!generated && !loading && (
                <div className="text-zinc-400">
                  <svg className="w-16 h-16 mx-auto mb-4 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <p>Document Preview</p>
                </div>
              )}

              {loading && (
                <div className="animate-pulse space-y-4 w-full px-8">
                  <div className="h-4 bg-zinc-200 dark:bg-zinc-800 rounded w-3/4 mx-auto"></div>
                  <div className="h-4 bg-zinc-200 dark:bg-zinc-800 rounded w-1/2 mx-auto"></div>
                  <div className="h-4 bg-zinc-200 dark:bg-zinc-800 rounded w-5/6 mx-auto"></div>
                </div>
              )}

              {generated && (
                <div className="animate-in fade-in zoom-in duration-300">
                  <div className="w-24 h-32 bg-zinc-100 dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 rounded mb-4 mx-auto shadow-sm flex items-center justify-center">
                    <span className="text-xs font-bold text-zinc-400">PDF</span>
                  </div>
                  <h3 className="font-medium text-lg text-green-600 dark:text-green-400">Generation Complete!</h3>
                  <div className="mt-4 flex gap-3 justify-center">
                    <button className="px-4 py-2 bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400 rounded-lg font-medium text-sm hover:bg-blue-100 dark:hover:bg-blue-900/40">
                      Download PDF
                    </button>
                    <button className="px-4 py-2 bg-zinc-100 dark:bg-zinc-800 rounded-lg font-medium text-sm hover:bg-zinc-200 dark:hover:bg-zinc-700">
                      Download DOCX
                    </button>
                  </div>
                </div>
              )}
            </div>
          </section>

        </div>
      </div>
    </main>
  );
}

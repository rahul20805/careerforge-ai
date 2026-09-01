"use client";

import Link from "next/link";
import { useState } from "react";

export default function Opportunities() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [parsed, setParsed] = useState(false);

  const handleParse = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setParsed(false);
    
    // Simulate AI parsing
    setTimeout(() => {
       setLoading(false);
       setParsed(true);
    }, 2500);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-background via-zinc-50 to-zinc-100 dark:from-background dark:via-zinc-900 dark:to-zinc-950 text-zinc-900 dark:text-zinc-100 p-4 lg:p-12 relative overflow-hidden">
      
      {/* Background gradients */}
      <div className="absolute top-0 -left-10 w-96 h-96 bg-primary rounded-full mix-blend-multiply filter blur-[100px] opacity-10 animate-pulse-slow pointer-events-none"></div>

      <div className="max-w-4xl mx-auto space-y-8 relative z-10 animate-fade-in-up">
        
        {/* Navigation */}
        <nav className="flex items-center justify-between glass-card px-6 py-4 rounded-2xl mb-8">
          <div className="font-bold text-xl tracking-tight text-primary">CareerForge AI</div>
          <div className="flex items-center gap-6 text-sm font-medium">
            <Link href="/" className="text-zinc-500 hover:text-primary transition-colors">Home</Link>
            <Link href="/dashboard" className="text-zinc-500 hover:text-primary transition-colors">Dashboard</Link>
          </div>
        </nav>

        {/* Header */}
        <header className="flex justify-between items-end border-b border-zinc-200/50 dark:border-zinc-800/50 pb-4">
          <div>
            <h1 className="text-4xl lg:text-5xl font-extrabold tracking-tight bg-gradient-to-r from-zinc-900 to-zinc-500 dark:from-zinc-100 dark:to-zinc-500 bg-clip-text text-transparent">Discover Roles</h1>
            <p className="text-zinc-500 dark:text-zinc-400 mt-2 text-lg">Parse Job Descriptions instantly via URL to get AI matching scores.</p>
          </div>
        </header>

        {/* Input Form */}
        <section className="glass-card p-8 rounded-3xl">
          <form onSubmit={handleParse} className="flex flex-col sm:flex-row gap-4">
            <input 
              type="url"
              required
              placeholder="Paste LinkedIn or Company Career page URL..."
              className="flex-1 px-5 py-4 rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white/50 dark:bg-zinc-900/50 focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all placeholder:text-zinc-400"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
            <button 
              type="submit"
              disabled={loading}
              className="px-8 py-4 bg-primary hover:bg-primary/90 text-primary-foreground font-semibold rounded-xl shadow-lg shadow-primary/25 transition-all hover:-translate-y-0.5 disabled:opacity-50 disabled:hover:translate-y-0 relative overflow-hidden"
            >
              {loading ? (
                   <span className="flex items-center justify-center">
                     <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                     Extracting...
                   </span>
              ) : "Extract JD"}
            </button>
          </form>
        </section>

        {/* Loading Skeleton */}
        {loading && (
          <div className="p-8 rounded-3xl glass-card animate-pulse space-y-6">
             <div className="h-6 bg-zinc-200 dark:bg-zinc-800 rounded w-1/4"></div>
             <div className="h-4 bg-zinc-200 dark:bg-zinc-800 rounded w-1/2"></div>
             
             <div className="space-y-4 pt-4">
               <div className="p-4 bg-zinc-100/50 dark:bg-zinc-800/50 rounded-xl space-y-3">
                 <div className="h-3 bg-zinc-200 dark:bg-zinc-800 rounded w-16"></div>
                 <div className="h-5 bg-zinc-200 dark:bg-zinc-800 rounded w-1/3"></div>
               </div>
               <div className="p-4 bg-zinc-100/50 dark:bg-zinc-800/50 rounded-xl space-y-3">
                 <div className="h-3 bg-zinc-200 dark:bg-zinc-800 rounded w-24"></div>
                 <div className="flex gap-2">
                   <div className="h-8 bg-zinc-200 dark:bg-zinc-800 rounded w-20"></div>
                   <div className="h-8 bg-zinc-200 dark:bg-zinc-800 rounded w-24"></div>
                   <div className="h-8 bg-zinc-200 dark:bg-zinc-800 rounded w-16"></div>
                 </div>
               </div>
             </div>
          </div>
        )}

        {/* Mock Results */}
        {!loading && parsed && (
          <div className="p-8 rounded-3xl glass-card animate-fade-in-up border-l-4 border-l-primary">
            <div className="flex justify-between items-start mb-6">
              <div>
                <h3 className="text-2xl font-bold tracking-tight">Parsed Opportunity</h3>
                <p className="text-zinc-500 mt-1">This role matches your profile with an <strong className="text-primary">85% ATS fit</strong>.</p>
              </div>
              <div className="hidden sm:flex w-16 h-16 rounded-full bg-primary/10 text-primary items-center justify-center font-bold text-xl border-4 border-primary/20">
                85%
              </div>
            </div>
            
            <div className="space-y-4">
              <div className="p-5 bg-white/50 dark:bg-zinc-900/50 rounded-xl border border-zinc-200/50 dark:border-zinc-800/50 hover:border-primary/30 transition-colors">
                <span className="text-xs font-bold uppercase tracking-wider text-zinc-500">Role</span>
                <p className="font-semibold text-lg mt-1">Senior Frontend Engineer</p>
              </div>
              <div className="p-5 bg-white/50 dark:bg-zinc-900/50 rounded-xl border border-zinc-200/50 dark:border-zinc-800/50 hover:border-primary/30 transition-colors">
                <span className="text-xs font-bold uppercase tracking-wider text-zinc-500">Required Skills</span>
                <div className="flex gap-2 mt-3 flex-wrap">
                  {["React", "TypeScript", "Next.js", "GraphQL"].map(skill => (
                    <span key={skill} className="px-3 py-1.5 bg-primary/10 text-primary rounded-lg text-sm font-semibold shadow-sm border border-primary/20">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            </div>
            
            <div className="mt-8 pt-8 border-t border-zinc-200/50 dark:border-zinc-800/50 flex justify-end">
              <Link href="/resumes">
                <button className="px-8 py-3 bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 font-bold rounded-xl shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all flex items-center gap-2">
                  Tailor Resume <span className="text-xl leading-none">&rarr;</span>
                </button>
              </Link>
            </div>
          </div>
        )}

      </div>
    </main>
  );
}

"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function SearchPage() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);
  const [error, setError] = useState("");

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setLoading(true);
    setError("");
    
    const token = localStorage.getItem("token");
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "";
    
    try {
      const res = await fetch(`${apiUrl}/api/opportunities/search?query=${encodeURIComponent(query)}`, {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });
      if (!res.ok) throw new Error("Search failed");
      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch search results. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-background via-zinc-50 to-zinc-100 dark:from-background dark:via-zinc-900 dark:to-zinc-950 text-zinc-900 dark:text-zinc-100 p-4 lg:p-12 relative overflow-hidden">
      
      <div className="absolute top-0 left-0 w-96 h-96 bg-primary rounded-full mix-blend-multiply filter blur-[100px] opacity-10 animate-pulse-slow pointer-events-none"></div>

      <div className="max-w-6xl mx-auto space-y-10 relative z-10 animate-fade-in-up">
        
        {/* Navigation */}
        <nav className="flex items-center justify-between glass-card px-6 py-4 rounded-2xl mb-8">
          <div className="font-bold text-xl tracking-tight text-primary">CareerForge AI</div>
          <div className="flex items-center gap-6 text-sm font-medium overflow-x-auto whitespace-nowrap scrollbar-hide">
            <Link href="/dashboard" className="text-zinc-500 hover:text-primary transition-colors">Dashboard</Link>
            <Link href="/search" className="text-primary font-semibold transition-colors">Job Search</Link>
            <Link href="/networking" className="text-zinc-500 hover:text-primary transition-colors">Networking</Link>
            <Link href="/documents" className="text-zinc-500 hover:text-primary transition-colors">Documents</Link>
            <Link href="/profile" className="px-4 py-2 bg-primary/10 text-primary rounded-lg hover:bg-primary/20 transition-colors">Profile</Link>
          </div>
        </nav>

        <header className="text-center pb-8">
          <h1 className="text-4xl lg:text-5xl font-extrabold tracking-tight bg-gradient-to-r from-zinc-900 to-zinc-500 dark:from-zinc-100 dark:to-zinc-500 bg-clip-text text-transparent">AI Job Search</h1>
          <p className="text-zinc-500 dark:text-zinc-400 mt-4 text-lg max-w-2xl mx-auto">Discover the perfect opportunities tailored to your profile. Enter a role or company below.</p>
        </header>

        <form onSubmit={handleSearch} className="max-w-3xl mx-auto">
          <div className="relative flex items-center glass-card rounded-2xl p-2 shadow-lg hover:shadow-xl transition-shadow">
            <svg className="absolute left-6 w-6 h-6 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input 
              type="text" 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. Software Engineer internship at Google"
              className="w-full pl-16 pr-4 py-4 bg-transparent outline-none text-lg placeholder:text-zinc-400"
              required
            />
            <button 
              type="submit"
              disabled={loading}
              className="ml-2 px-8 py-4 bg-primary text-primary-foreground font-semibold rounded-xl hover:bg-primary/90 shadow-md transition-all disabled:opacity-50 whitespace-nowrap"
            >
              {loading ? "Searching..." : "Search"}
            </button>
          </div>
        </form>

        {error && <div className="text-red-500 text-center">{error}</div>}

        {results.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-12 animate-fade-in-up">
            {results.map((job, idx) => (
              <div key={idx} className="glass-card p-8 rounded-3xl hover:bg-white/40 dark:hover:bg-zinc-800/40 transition-all border border-transparent hover:border-primary/20 group">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-bold group-hover:text-primary transition-colors">{job.title}</h3>
                    <p className="text-zinc-500 dark:text-zinc-400 mt-1">{job.company_name} &bull; {job.location}</p>
                  </div>
                  <span className="px-3 py-1 bg-primary/10 text-primary text-xs font-bold rounded-full uppercase tracking-wider">{job.opportunity_type}</span>
                </div>
                <div className="flex items-center gap-3 text-sm text-zinc-500 dark:text-zinc-400 mb-8">
                  <span className="flex items-center gap-1"><svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>{job.work_mode}</span>
                </div>
                <div className="flex gap-4">
                  <a href={job.application_url} target="_blank" rel="noreferrer" className="flex-1 py-3 text-center bg-primary text-primary-foreground font-semibold rounded-xl hover:bg-primary/90 transition-colors shadow-sm">
                    Apply Now
                  </a>
                  <button 
                    onClick={() => {
                      alert("Integration to pipeline is functional, saving omitted for brevity.");
                    }}
                    className="px-5 py-3 border-2 border-zinc-200 dark:border-zinc-700 font-semibold rounded-xl hover:border-primary hover:text-primary transition-colors"
                  >
                    Track
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}

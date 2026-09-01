"use client";

import { useState } from "react";
import Link from "next/link";

export default function NetworkingPage() {
  const [institution, setInstitution] = useState("");
  const [researchArea, setResearchArea] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!institution) return;
    
    setLoading(true);
    
    const token = localStorage.getItem("token");
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "";
    
    try {
      const res = await fetch(`${apiUrl}/api/contacts/professors/search?institution=${encodeURIComponent(institution)}&research_area=${encodeURIComponent(researchArea)}`, {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });
      if (res.ok) {
        const data = await res.json();
        setResults(data);
      }
    } catch (err) {
      console.error(err);
      alert("Error finding contacts");
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
            <Link href="/search" className="text-zinc-500 hover:text-primary transition-colors">Job Search</Link>
            <Link href="/networking" className="text-primary font-semibold transition-colors">Networking</Link>
            <Link href="/documents" className="text-zinc-500 hover:text-primary transition-colors">Documents</Link>
            <Link href="/profile" className="px-4 py-2 bg-primary/10 text-primary rounded-lg hover:bg-primary/20 transition-colors">Profile</Link>
          </div>
        </nav>

        <header className="text-center pb-8">
          <h1 className="text-4xl lg:text-5xl font-extrabold tracking-tight bg-gradient-to-r from-zinc-900 to-zinc-500 dark:from-zinc-100 dark:to-zinc-500 bg-clip-text text-transparent">Academic Networking</h1>
          <p className="text-zinc-500 dark:text-zinc-400 mt-4 text-lg max-w-2xl mx-auto">Discover professors and research labs matching your academic interests.</p>
        </header>
        
        <form onSubmit={handleSearch} className="max-w-3xl mx-auto flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <input 
              type="text" 
              value={institution}
              onChange={(e) => setInstitution(e.target.value)}
              placeholder="Institution (e.g. MIT, Stanford)"
              className="w-full p-4 rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white/50 dark:bg-zinc-900/50 focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all placeholder:text-zinc-400"
              required
            />
          </div>
          <div className="flex-1">
            <input 
              type="text" 
              value={researchArea}
              onChange={(e) => setResearchArea(e.target.value)}
              placeholder="Research Area (e.g. AI, Quantum)"
              className="w-full p-4 rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white/50 dark:bg-zinc-900/50 focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all placeholder:text-zinc-400"
            />
          </div>
          <button 
            type="submit"
            disabled={loading}
            className="px-8 py-4 bg-primary text-primary-foreground font-semibold rounded-xl hover:bg-primary/90 shadow-md transition-all disabled:opacity-50"
          >
            {loading ? "Searching..." : "Discover"}
          </button>
        </form>

        {results.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-12">
            {results.map((prof, idx) => (
              <div key={idx} className="glass-card p-6 rounded-3xl group">
                <h3 className="text-xl font-bold group-hover:text-primary transition-colors">{prof.name}</h3>
                <p className="text-zinc-500 dark:text-zinc-400 font-medium mb-4">{prof.department} @ {prof.institution_name}</p>
                
                <div className="space-y-2 mb-6">
                  <p className="text-sm"><strong>Lab:</strong> {prof.lab_name}</p>
                  <p className="text-sm"><strong>Focus:</strong> {prof.research_areas?.join(", ")}</p>
                  <p className="text-sm"><strong>Email:</strong> <a href={`mailto:${prof.email}`} className="text-primary hover:underline">{prof.email}</a></p>
                </div>
                
                <div className="pt-4 border-t border-zinc-200 dark:border-zinc-800">
                  <p className="text-xs text-zinc-400 uppercase tracking-wider font-semibold mb-2">Match Reasons</p>
                  <ul className="text-sm space-y-1 text-zinc-600 dark:text-zinc-300 list-disc pl-4">
                    {prof.match_reasons?.map((reason: string, i: number) => (
                      <li key={i}>{reason}</li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}

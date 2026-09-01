"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function DocumentsPage() {
  const [docType, setDocType] = useState("SOP");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState("");
  
  // SOP specific
  const [targetProgram, setTargetProgram] = useState("");
  const [targetInstitute, setTargetInstitute] = useState("");
  const [tone, setTone] = useState("Academic");

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResult("");
    
    const token = localStorage.getItem("token");
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "";
    
    let endpoint = "";
    let payload = {};
    
    if (docType === "SOP") {
      endpoint = "/api/documents/sop/generate";
      payload = {
        target_program: targetProgram,
        target_institute: targetInstitute,
        tone: tone
      };
    } else {
      // Stub for LOR and Email
      endpoint = "/api/documents/email/generate";
      payload = {
        email_type: "HR internship",
        tone: tone
      };
    }
    
    try {
      const res = await fetch(`${apiUrl}${endpoint}`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });
      
      if (!res.ok) throw new Error("Generation failed");
      const data = await res.json();
      setResult(data.content || data.body || "Generated successfully but no content returned.");
    } catch (err) {
      console.error(err);
      alert("Error generating document");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-background via-zinc-50 to-zinc-100 dark:from-background dark:via-zinc-900 dark:to-zinc-950 text-zinc-900 dark:text-zinc-100 p-4 lg:p-12 relative overflow-hidden">
      
      <div className="absolute top-0 right-0 w-96 h-96 bg-primary rounded-full mix-blend-multiply filter blur-[100px] opacity-10 animate-pulse-slow pointer-events-none"></div>

      <div className="max-w-6xl mx-auto space-y-10 relative z-10 animate-fade-in-up">
        
        {/* Navigation */}
        <nav className="flex items-center justify-between glass-card px-6 py-4 rounded-2xl mb-8">
          <div className="font-bold text-xl tracking-tight text-primary">CareerForge AI</div>
          <div className="flex items-center gap-6 text-sm font-medium overflow-x-auto whitespace-nowrap scrollbar-hide">
            <Link href="/dashboard" className="text-zinc-500 hover:text-primary transition-colors">Dashboard</Link>
            <Link href="/search" className="text-zinc-500 hover:text-primary transition-colors">Job Search</Link>
            <Link href="/networking" className="text-zinc-500 hover:text-primary transition-colors">Networking</Link>
            <Link href="/documents" className="text-primary font-semibold transition-colors">Documents</Link>
            <Link href="/profile" className="px-4 py-2 bg-primary/10 text-primary rounded-lg hover:bg-primary/20 transition-colors">Profile</Link>
          </div>
        </nav>

        <header className="pb-8 border-b border-zinc-200 dark:border-zinc-800">
          <h1 className="text-4xl lg:text-5xl font-extrabold tracking-tight bg-gradient-to-r from-zinc-900 to-zinc-500 dark:from-zinc-100 dark:to-zinc-500 bg-clip-text text-transparent">AI Documents</h1>
          <p className="text-zinc-500 dark:text-zinc-400 mt-4 text-lg">Generate hyper-personalized Statement of Purposes, Letters of Recommendation, and Outreach Emails instantly.</p>
        </header>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
          <div className="lg:col-span-1 space-y-6">
            <div className="glass-card p-6 rounded-3xl">
              <h2 className="text-xl font-bold mb-4">Configuration</h2>
              
              <div className="flex gap-2 mb-6 bg-zinc-100 dark:bg-zinc-800 p-1.5 rounded-xl">
                {["SOP", "LOR", "Email"].map(type => (
                  <button 
                    key={type}
                    onClick={() => setDocType(type)}
                    className={`flex-1 py-2 rounded-lg font-medium text-sm transition-all ${docType === type ? 'bg-white dark:bg-zinc-700 shadow-sm' : 'text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300'}`}
                  >
                    {type}
                  </button>
                ))}
              </div>
              
              <form onSubmit={handleGenerate} className="space-y-4">
                {docType === "SOP" && (
                  <>
                    <div>
                      <label className="block text-sm font-semibold mb-1.5">Target Program</label>
                      <input type="text" value={targetProgram} onChange={e => setTargetProgram(e.target.value)} required placeholder="MSc Computer Science" className="w-full p-3 rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white/50 dark:bg-zinc-900/50 outline-none" />
                    </div>
                    <div>
                      <label className="block text-sm font-semibold mb-1.5">Target Institute</label>
                      <input type="text" value={targetInstitute} onChange={e => setTargetInstitute(e.target.value)} required placeholder="Stanford University" className="w-full p-3 rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white/50 dark:bg-zinc-900/50 outline-none" />
                    </div>
                  </>
                )}
                
                <div>
                  <label className="block text-sm font-semibold mb-1.5">Tone</label>
                  <select value={tone} onChange={e => setTone(e.target.value)} className="w-full p-3 rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white/50 dark:bg-zinc-900/50 outline-none">
                    <option>Academic</option>
                    <option>Professional</option>
                    <option>Enthusiastic</option>
                  </select>
                </div>
                
                <button type="submit" disabled={loading} className="w-full py-4 mt-4 bg-primary text-primary-foreground font-bold rounded-xl shadow-lg hover:bg-primary/90 disabled:opacity-50">
                  {loading ? "Synthesizing..." : `Generate ${docType}`}
                </button>
              </form>
            </div>
          </div>
          
          <div className="lg:col-span-2">
            <div className="glass-card p-8 rounded-3xl h-full min-h-[500px] flex flex-col">
              <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                <svg className="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                Output Document
              </h2>
              
              {result ? (
                <div className="flex-1 bg-white/50 dark:bg-zinc-900/50 rounded-2xl p-6 border border-zinc-200 dark:border-zinc-800 overflow-y-auto whitespace-pre-wrap leading-relaxed text-sm">
                  {result}
                </div>
              ) : (
                <div className="flex-1 flex flex-col items-center justify-center text-zinc-400">
                  <svg className="w-16 h-16 mb-4 opacity-20" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" /></svg>
                  <p>Configure parameters and click Generate to see the AI output here.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

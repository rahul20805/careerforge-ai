"use client";

import Link from "next/link";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Dashboard() {
  const router = useRouter();
  const [applications, setApplications] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  const [showModal, setShowModal] = useState(false);
  const [newAppUrl, setNewAppUrl] = useState("");
  const [newAppTitle, setNewAppTitle] = useState("");
  const [newAppCompany, setNewAppCompany] = useState("");
  const [isUrlMode, setIsUrlMode] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }
    
    fetchApplications(token);
  }, [router]);

  const fetchApplications = async (token: string) => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "";
    try {
      const res = await fetch(`${apiUrl}/api/applications/`, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setApplications(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleNewApplication = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    
    const token = localStorage.getItem("token");
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "";
    
    try {
      let oppData;
      
      if (isUrlMode && newAppUrl) {
        // Parse and create from URL
        const parseRes = await fetch(`${apiUrl}/api/opportunities/parse`, {
          method: "POST",
          headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" },
          body: JSON.stringify({ url: newAppUrl, source_type: "URL" })
        });
        
        if (!parseRes.ok) throw new Error("Failed to parse URL");
        oppData = await parseRes.json();
      } else {
        // Create manual opportunity
        oppData = {
          title: newAppTitle,
          company_name: newAppCompany,
          status: "OPEN",
          source_type: "MANUAL",
          requirements: []
        };
      }
      
      // Save opportunity
      const createOppRes = await fetch(`${apiUrl}/api/opportunities/`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" },
        body: JSON.stringify(oppData)
      });
      
      if (!createOppRes.ok) throw new Error("Failed to create opportunity");
      const savedOpp = await createOppRes.json();
      
      // Create application
      const createAppRes = await fetch(`${apiUrl}/api/applications/`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" },
        body: JSON.stringify({ opportunity_id: savedOpp.id, status: "APPLIED" })
      });
      
      if (!createAppRes.ok) throw new Error("Failed to create application");
      
      setShowModal(false);
      setNewAppUrl("");
      setNewAppTitle("");
      setNewAppCompany("");
      
      if (token) fetchApplications(token);
      
    } catch (err) {
      console.error(err);
      alert("Error creating application.");
    } finally {
      setSubmitting(false);
    }
  };

  const activeAppsCount = applications.filter(a => !["REJECTED", "WITHDRAWN", "CLOSED"].includes(a.status)).length;
  const interviewCount = applications.filter(a => a.status === "INTERVIEW").length;

  const metrics = [
    { label: "Active Applications", value: activeAppsCount, trend: "Current Pipeline" },
    { label: "Upcoming Interviews", value: interviewCount, trend: "Scheduled" },
    { label: "Total Tracked", value: applications.length, trend: "All Time" },
    { label: "Average ATS Score", value: "88%", trend: "Top 10% of users" },
  ];

  const getColorForStatus = (status: string) => {
    switch (status) {
      case "INTERVIEW": return "bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300";
      case "APPLIED": return "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300";
      case "SCREENING": return "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300";
      case "OFFER": return "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300";
      default: return "bg-zinc-100 text-zinc-700 dark:bg-zinc-900/30 dark:text-zinc-300";
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-background via-zinc-50 to-zinc-100 dark:from-background dark:via-zinc-900 dark:to-zinc-950 text-zinc-900 dark:text-zinc-100 p-4 lg:p-12 relative overflow-hidden">
      
      {/* Background gradients */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-primary rounded-full mix-blend-multiply filter blur-[100px] opacity-10 animate-pulse-slow pointer-events-none"></div>

      <div className="max-w-7xl mx-auto space-y-10 relative z-10 animate-fade-in-up">
        
        {/* Navigation Bar */}
        <nav className="flex items-center justify-between glass-card px-6 py-4 rounded-2xl mb-8">
          <div className="font-bold text-xl tracking-tight text-primary">CareerForge AI</div>
          <div className="flex items-center gap-6 text-sm font-medium">
            <Link href="/" className="text-zinc-500 hover:text-primary transition-colors">Home</Link>
            <Link href="/opportunities" className="text-zinc-500 hover:text-primary transition-colors">Opportunities</Link>
            <Link href="/resumes" className="text-zinc-500 hover:text-primary transition-colors">Resumes</Link>
            <Link href="/profile" className="px-4 py-2 bg-primary/10 text-primary rounded-lg hover:bg-primary/20 transition-colors">My Profile</Link>
          </div>
        </nav>

        {/* Header */}
        <header className="flex justify-between items-end pb-4 border-b border-zinc-200/50 dark:border-zinc-800/50">
          <div>
            <h1 className="text-4xl lg:text-5xl font-extrabold tracking-tight bg-gradient-to-r from-zinc-900 to-zinc-500 dark:from-zinc-100 dark:to-zinc-500 bg-clip-text text-transparent">Overview</h1>
            <p className="text-zinc-500 dark:text-zinc-400 mt-2 text-lg">Your career pipeline at a glance.</p>
          </div>
          <button 
            onClick={() => setShowModal(true)}
            className="hidden lg:flex items-center gap-2 px-5 py-2.5 bg-primary text-white rounded-xl font-medium shadow-lg shadow-primary/20 hover:-translate-y-0.5 transition-all"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
            New Application
          </button>
        </header>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {metrics.map((m, i) => (
            <div key={i} className="glass-card p-6 rounded-2xl flex flex-col justify-between group">
              <p className="text-sm text-zinc-500 dark:text-zinc-400 font-semibold uppercase tracking-wider">{m.label}</p>
              <div className="mt-4">
                <p className="text-4xl font-extrabold text-zinc-900 dark:text-zinc-100 group-hover:text-primary transition-colors">{m.value}</p>
                <p className="text-sm font-medium text-zinc-500 dark:text-zinc-500 mt-2">{m.trend}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Pipeline Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          <div className="lg:col-span-2 space-y-6">
            <h2 className="text-2xl font-bold tracking-tight">Active Pipeline</h2>
            <section className="glass-card rounded-3xl overflow-hidden min-h-[300px]">
              {loading ? (
                <div className="p-8 flex justify-center items-center h-full">
                  <span className="text-zinc-500 animate-pulse">Loading applications...</span>
                </div>
              ) : applications.length === 0 ? (
                <div className="p-12 flex flex-col justify-center items-center h-full text-center">
                  <p className="text-zinc-500 mb-4">No applications tracked yet.</p>
                  <button 
                    onClick={() => setShowModal(true)}
                    className="px-5 py-2.5 bg-primary text-white rounded-xl font-medium shadow-lg hover:bg-primary/90"
                  >
                    Add your first application
                  </button>
                </div>
              ) : (
                <div className="divide-y divide-zinc-200/50 dark:divide-zinc-800/50">
                  {applications.map((app, i) => (
                    <div key={i} className="p-6 flex flex-col sm:flex-row sm:justify-between sm:items-center hover:bg-white/40 dark:hover:bg-zinc-800/40 transition-colors group cursor-pointer">
                      <div className="mb-4 sm:mb-0">
                        <h3 className="font-bold text-lg group-hover:text-primary transition-colors">{app.opportunity?.title || "Unknown Role"}</h3>
                        <p className="text-zinc-500 dark:text-zinc-400 text-sm font-medium mt-1">{app.opportunity?.company_name || "Unknown Company"}</p>
                      </div>
                      <div className="flex items-center gap-4 text-sm">
                        <span className={`px-4 py-1.5 rounded-full font-bold text-xs tracking-wide uppercase ${getColorForStatus(app.status)}`}>
                          {app.status}
                        </span>
                        <span className="text-zinc-400 font-medium flex items-center gap-1.5">
                          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                          {new Date(app.created_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </div>

          <div className="space-y-6">
            <h2 className="text-2xl font-bold tracking-tight">Recent Activity</h2>
            <section className="glass-card rounded-3xl p-6 h-full min-h-[300px] flex flex-col items-center justify-center text-center">
               <div className="w-16 h-16 bg-primary/10 text-primary rounded-full flex items-center justify-center mb-4">
                 <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
               </div>
               <h3 className="text-lg font-bold">All caught up!</h3>
               <p className="text-zinc-500 text-sm mt-2 max-w-[200px]">You&apos;ve reviewed all your recent application updates.</p>
            </section>
          </div>

        </div>

      </div>

      {/* New Application Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="bg-white dark:bg-zinc-900 rounded-3xl p-8 max-w-lg w-full shadow-2xl relative animate-fade-in-up">
            <button 
              onClick={() => setShowModal(false)}
              className="absolute top-6 right-6 text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200"
            >
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
            <h2 className="text-2xl font-bold mb-6">Track New Application</h2>
            
            <div className="flex gap-4 mb-6 bg-zinc-100 dark:bg-zinc-800 p-1.5 rounded-xl">
              <button 
                onClick={() => setIsUrlMode(true)}
                className={`flex-1 py-2 rounded-lg font-medium text-sm transition-all ${isUrlMode ? 'bg-white dark:bg-zinc-700 shadow-sm' : 'text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300'}`}
              >
                From URL
              </button>
              <button 
                onClick={() => setIsUrlMode(false)}
                className={`flex-1 py-2 rounded-lg font-medium text-sm transition-all ${!isUrlMode ? 'bg-white dark:bg-zinc-700 shadow-sm' : 'text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300'}`}
              >
                Manual Entry
              </button>
            </div>
            
            <form onSubmit={handleNewApplication} className="space-y-4">
              {isUrlMode ? (
                <div>
                  <label className="block text-sm font-semibold text-zinc-700 dark:text-zinc-300 mb-2">Job Description URL</label>
                  <input 
                    type="url" 
                    required 
                    value={newAppUrl}
                    onChange={(e) => setNewAppUrl(e.target.value)}
                    placeholder="https://linkedin.com/jobs/..."
                    className="w-full p-3 rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white/50 dark:bg-zinc-900/50 focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all"
                  />
                  <p className="text-xs text-zinc-500 mt-2">We will automatically parse the role, company, and requirements.</p>
                </div>
              ) : (
                <>
                  <div>
                    <label className="block text-sm font-semibold text-zinc-700 dark:text-zinc-300 mb-2">Job Title</label>
                    <input 
                      type="text" 
                      required 
                      value={newAppTitle}
                      onChange={(e) => setNewAppTitle(e.target.value)}
                      placeholder="e.g. Senior Frontend Engineer"
                      className="w-full p-3 rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white/50 dark:bg-zinc-900/50 focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-zinc-700 dark:text-zinc-300 mb-2">Company Name</label>
                    <input 
                      type="text" 
                      required 
                      value={newAppCompany}
                      onChange={(e) => setNewAppCompany(e.target.value)}
                      placeholder="e.g. Google"
                      className="w-full p-3 rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white/50 dark:bg-zinc-900/50 focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all"
                    />
                  </div>
                </>
              )}
              
              <button 
                type="submit"
                disabled={submitting}
                className="w-full mt-6 py-4 bg-primary text-primary-foreground font-semibold rounded-xl hover:bg-primary/90 shadow-lg shadow-primary/30 transition-all disabled:opacity-50"
              >
                {submitting ? "Saving..." : "Add to Pipeline"}
              </button>
            </form>
          </div>
        </div>
      )}
    </main>
  );
}

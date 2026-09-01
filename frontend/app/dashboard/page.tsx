import Link from "next/link";

export default function Dashboard() {
  // Static mockup data, normally fetched via API
  const metrics = [
    { label: "Active Applications", value: 12, trend: "+2 this week" },
    { label: "Upcoming Interviews", value: 2, trend: "Next: Google (Oct 12)" },
    { label: "Resumes Generated", value: 24, trend: "View History" },
    { label: "Average ATS Score", value: "88%", trend: "Top 10% of users" },
  ];

  const pipeline = [
    { company: "Google", role: "Software Engineer", status: "Interview", date: "Oct 12", color: "bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300" },
    { company: "Stanford Lab", role: "Research Assistant", status: "Applied", date: "Oct 10", color: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300" },
    { company: "Stripe", role: "Backend Engineer", status: "Screening", date: "Oct 15", color: "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300" },
  ];

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
          <button className="hidden lg:flex items-center gap-2 px-5 py-2.5 bg-primary text-white rounded-xl font-medium shadow-lg shadow-primary/20 hover:-translate-y-0.5 transition-all">
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
            <section className="glass-card rounded-3xl overflow-hidden">
              <div className="divide-y divide-zinc-200/50 dark:divide-zinc-800/50">
                {pipeline.map((job, i) => (
                  <div key={i} className="p-6 flex flex-col sm:flex-row sm:justify-between sm:items-center hover:bg-white/40 dark:hover:bg-zinc-800/40 transition-colors group cursor-pointer">
                    <div className="mb-4 sm:mb-0">
                      <h3 className="font-bold text-lg group-hover:text-primary transition-colors">{job.role}</h3>
                      <p className="text-zinc-500 dark:text-zinc-400 text-sm font-medium mt-1">{job.company}</p>
                    </div>
                    <div className="flex items-center gap-4 text-sm">
                      <span className={`px-4 py-1.5 rounded-full font-bold text-xs tracking-wide uppercase ${job.color}`}>
                        {job.status}
                      </span>
                      <span className="text-zinc-400 font-medium flex items-center gap-1.5">
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                        {job.date}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
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
    </main>
  );
}

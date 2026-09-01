import Link from "next/link";

export default function Dashboard() {
  // Static mockup data, normally fetched via API
  const metrics = [
    { label: "Active Applications", value: 12 },
    { label: "Upcoming Interviews", value: 2 },
    { label: "Resumes Generated", value: 24 },
    { label: "Average ATS Score", value: "88%" },
  ];

  const pipeline = [
    { company: "Google", role: "Software Engineer", status: "Interview", date: "Oct 12" },
    { company: "Stanford Lab", role: "Research Assistant", status: "Applied", date: "Oct 10" },
    { company: "Stripe", role: "Backend Engineer", status: "Screening", date: "Oct 15" },
  ];

  return (
    <main className="min-h-screen bg-zinc-50 dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100 p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="flex justify-between items-end border-b border-zinc-200 dark:border-zinc-800 pb-4">
          <div>
            <h1 className="text-4xl font-bold tracking-tight">Dashboard</h1>
            <p className="text-zinc-500 mt-1">Welcome back. Here is an overview of your career pipeline.</p>
          </div>
          <Link href="/" className="text-sm font-medium hover:underline text-blue-600 dark:text-blue-400">
            &larr; Back Home
          </Link>
        </header>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {metrics.map((m, i) => (
            <div key={i} className="p-6 rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 shadow-sm">
              <p className="text-sm text-zinc-500 dark:text-zinc-400 font-medium">{m.label}</p>
              <p className="text-3xl font-bold mt-2">{m.value}</p>
            </div>
          ))}
        </div>

        {/* Pipeline Section */}
        <section className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-sm overflow-hidden">
          <div className="p-6 border-b border-zinc-200 dark:border-zinc-800">
            <h2 className="text-xl font-semibold">Active Pipeline</h2>
          </div>
          <div className="divide-y divide-zinc-200 dark:divide-zinc-800">
            {pipeline.map((job, i) => (
              <div key={i} className="p-6 flex justify-between items-center hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors">
                <div>
                  <h3 className="font-semibold text-lg">{job.role}</h3>
                  <p className="text-zinc-500 text-sm">{job.company}</p>
                </div>
                <div className="flex items-center gap-6 text-sm">
                  <span className="px-3 py-1 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 font-medium">
                    {job.status}
                  </span>
                  <span className="text-zinc-400">{job.date}</span>
                </div>
              </div>
            ))}
          </div>
        </section>

      </div>
    </main>
  );
}

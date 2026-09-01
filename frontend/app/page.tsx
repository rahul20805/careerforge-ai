import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-6 lg:p-24 bg-gradient-to-br from-background via-zinc-100 to-zinc-200 dark:from-background dark:via-zinc-900 dark:to-black relative overflow-hidden">
      
      {/* Animated Background Gradients */}
      <div className="absolute top-0 -left-4 w-72 h-72 bg-primary rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse-slow"></div>
      <div className="absolute top-0 -right-4 w-72 h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse-slow" style={{ animationDelay: '2s' }}></div>
      <div className="absolute -bottom-8 left-20 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse-slow" style={{ animationDelay: '4s' }}></div>

      <div className="z-10 w-full max-w-6xl flex flex-col items-center justify-center animate-fade-in-up">
        
        <div className="mb-12 inline-flex items-center px-4 py-1.5 rounded-full border border-primary/20 bg-primary/10 text-primary text-sm font-medium shadow-sm backdrop-blur-md">
          <span className="relative flex h-2 w-2 mr-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
          </span>
          CareerForge AI is Live
        </div>

        <h1 className="text-5xl lg:text-7xl font-extrabold tracking-tight text-center text-zinc-900 dark:text-white max-w-4xl leading-tight drop-shadow-sm">
          Master Your Career Journey with <span className="bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">AI Precision</span>
        </h1>
        
        <p className="mt-6 text-lg lg:text-xl text-center text-zinc-600 dark:text-zinc-400 max-w-2xl text-balance">
          Automate your job search, generate truth-verified ATS resumes, and build your master profile using advanced AI technology.
        </p>

        <div className="mt-10 flex gap-4 mb-24">
          <Link href="/login">
            <button className="px-8 py-4 bg-primary text-primary-foreground font-semibold rounded-xl hover:bg-primary/90 shadow-lg shadow-primary/30 transition-all hover:-translate-y-1">
              Get Started for Free
            </button>
          </Link>
          <Link href="/dashboard">
            <button className="px-8 py-4 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 font-semibold rounded-xl border border-zinc-200 dark:border-zinc-700 hover:bg-zinc-50 dark:hover:bg-zinc-700 transition-all shadow-sm">
              View Dashboard
            </button>
          </Link>
        </div>

        <div className="w-full grid gap-6 lg:grid-cols-4 lg:gap-8">
          {[
            {
              title: "Smart Dashboard",
              href: "/dashboard",
              desc: "Track your application pipeline with dynamic AI insights.",
              icon: "📊"
            },
            {
              title: "Discover Roles",
              href: "/opportunities",
              desc: "Parse job descriptions instantly and match them against your profile.",
              icon: "🔍"
            },
            {
              title: "Verify Resumes",
              href: "/resumes",
              desc: "Generate ATS-beating resumes backed by your verified truth logic.",
              icon: "📄"
            },
            {
              title: "Master Profile",
              href: "/profile",
              desc: "Store your career history securely as a single source of truth.",
              icon: "👤"
            }
          ].map((item, i) => (
            <Link key={i} href={item.href} className="group glass-card p-6 rounded-2xl flex flex-col justify-between">
              <div>
                <div className="text-3xl mb-4 opacity-80 group-hover:opacity-100 transition-opacity">{item.icon}</div>
                <h2 className="text-xl font-bold mb-2 text-zinc-800 dark:text-zinc-200 group-hover:text-primary transition-colors">
                  {item.title}
                </h2>
                <p className="text-sm text-zinc-500 dark:text-zinc-400 leading-relaxed">
                  {item.desc}
                </p>
              </div>
              <div className="mt-6 flex items-center text-primary text-sm font-semibold opacity-0 group-hover:opacity-100 transition-all -translate-x-2 group-hover:translate-x-0">
                Explore <span className="ml-1">&rarr;</span>
              </div>
            </Link>
          ))}
        </div>

      </div>
    </main>
  );
}

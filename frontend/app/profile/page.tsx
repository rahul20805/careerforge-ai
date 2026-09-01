"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

interface UserProfile {
  headline?: string;
  summary?: string;
  phone?: string;
  city?: string;
  country?: string;
}

export default function Profile() {
  const router = useRouter();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    const fetchProfile = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        router.push("/login");
        return;
      }
      
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "";
      try {
        const res = await fetch(`${apiUrl}/api/profile/`, {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });
        if (res.ok) {
          const data = await res.json();
          setProfile(data);
        } else {
          router.push("/login");
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, [router]);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    const token = localStorage.getItem("token");
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "";
    
    try {
      const res = await fetch(`${apiUrl}/api/profile/`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(profile)
      });
      if (res.ok) {
        alert("Profile Saved Successfully!");
      } else {
        alert("Failed to save profile.");
      }
    } catch (err) {
      alert("Failed to save profile.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return (
    <div className="min-h-screen bg-gradient-to-br from-background via-zinc-50 to-zinc-100 flex items-center justify-center">
       <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-zinc-50 to-zinc-100 dark:from-background dark:via-zinc-900 dark:to-zinc-950 p-4 lg:p-12 relative overflow-hidden">
      
      {/* Background gradients */}
      <div className="absolute top-0 right-1/4 w-96 h-96 bg-primary rounded-full mix-blend-multiply filter blur-[100px] opacity-10 animate-pulse-slow pointer-events-none"></div>

      <div className="max-w-4xl mx-auto space-y-8 relative z-10 animate-fade-in-up">
        
        {/* Navigation */}
        <nav className="flex items-center justify-between glass-card px-6 py-4 rounded-2xl mb-8">
          <div className="font-bold text-xl tracking-tight text-primary">CareerForge AI</div>
          <div className="flex items-center gap-6 text-sm font-medium">
            <Link href="/" className="text-zinc-500 hover:text-primary transition-colors">Home</Link>
            <Link href="/dashboard" className="text-zinc-500 hover:text-primary transition-colors">Dashboard</Link>
          </div>
        </nav>
        
        <header className="flex justify-between items-end border-b border-zinc-200/50 dark:border-zinc-800/50 pb-4">
          <div>
            <h1 className="text-4xl lg:text-5xl font-extrabold tracking-tight bg-gradient-to-r from-zinc-900 to-zinc-500 dark:from-zinc-100 dark:to-zinc-500 bg-clip-text text-transparent">Master Profile</h1>
            <p className="text-zinc-500 dark:text-zinc-400 mt-2 text-lg">Manage your verified data that powers all AI generation.</p>
          </div>
        </header>

        <div className="glass-card rounded-3xl p-8">
          <form onSubmit={handleSave} className="space-y-6">
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-semibold text-zinc-700 dark:text-zinc-300 mb-2">Headline</label>
                <input 
                  type="text" 
                  value={profile?.headline || ""}
                  onChange={e => setProfile({...profile, headline: e.target.value})}
                  className="w-full px-5 py-4 rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white/50 dark:bg-zinc-900/50 focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all placeholder:text-zinc-400"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-zinc-700 dark:text-zinc-300 mb-2">Phone</label>
                <input 
                  type="text" 
                  value={profile?.phone || ""}
                  onChange={e => setProfile({...profile, phone: e.target.value})}
                  className="w-full px-5 py-4 rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white/50 dark:bg-zinc-900/50 focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all placeholder:text-zinc-400"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-semibold text-zinc-700 dark:text-zinc-300 mb-2">City</label>
                <input 
                  type="text" 
                  value={profile?.city || ""}
                  onChange={e => setProfile({...profile, city: e.target.value})}
                  className="w-full px-5 py-4 rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white/50 dark:bg-zinc-900/50 focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all placeholder:text-zinc-400"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-zinc-700 dark:text-zinc-300 mb-2">Country</label>
                <input 
                  type="text" 
                  value={profile?.country || ""}
                  onChange={e => setProfile({...profile, country: e.target.value})}
                  className="w-full px-5 py-4 rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white/50 dark:bg-zinc-900/50 focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all placeholder:text-zinc-400"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-zinc-700 dark:text-zinc-300 mb-2">Professional Summary</label>
              <textarea 
                rows={4}
                value={profile?.summary || ""}
                onChange={e => setProfile({...profile, summary: e.target.value})}
                className="w-full px-5 py-4 rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white/50 dark:bg-zinc-900/50 focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all placeholder:text-zinc-400"
                placeholder="A brief overview of your professional background..."
              />
            </div>

            <div className="flex justify-end pt-6 border-t border-zinc-200/50 dark:border-zinc-800/50">
              <button 
                type="submit" 
                disabled={saving}
                className="px-8 py-4 bg-primary text-primary-foreground font-semibold rounded-xl hover:bg-primary/90 shadow-lg shadow-primary/30 transition-all hover:-translate-y-0.5 disabled:opacity-50 disabled:hover:translate-y-0 relative overflow-hidden"
              >
                {saving ? (
                   <span className="flex items-center justify-center">
                     <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                     Saving...
                   </span>
                ) : "Save Master Profile"}
              </button>
            </div>
          </form>
        </div>

      </div>
    </div>
  );
}

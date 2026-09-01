"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function Login() {
  const router = useRouter();
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    // Use environment variable for API URL or default to empty string for relative paths in Vercel
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "";
    const endpoint = isLogin ? "/api/auth/login" : "/api/auth/register";

    try {
      let response;
      if (isLogin) {
        // OAuth2PasswordRequestForm expects form data
        const formData = new URLSearchParams();
        formData.append("username", email);
        formData.append("password", password);

        response = await fetch(`${apiUrl}${endpoint}`, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: formData.toString(),
        });
      } else {
        // Register expects JSON
        response = await fetch(`${apiUrl}${endpoint}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        });
      }

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Authentication failed");
      }

      // Save JWT token
      localStorage.setItem("token", data.access_token);
      
      // Redirect to dashboard
      router.push("/dashboard");

    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError(String(err));
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-zinc-50 dark:bg-zinc-950 flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white dark:bg-zinc-900 rounded-2xl shadow-xl border border-zinc-200 dark:border-zinc-800 p-8">
        
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-zinc-900 dark:text-zinc-100">
            {isLogin ? "Welcome back" : "Create an account"}
          </h1>
          <p className="text-zinc-500 mt-2 text-sm">
            {isLogin ? "Sign in to your CareerForge AI account." : "Start building your AI-optimized career today."}
          </p>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400 text-sm border border-red-200 dark:border-red-800">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1">Email</label>
            <input 
              type="email" 
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-transparent focus:ring-2 focus:ring-blue-500 outline-none"
              placeholder="you@example.com"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1">Password</label>
            <input 
              type="password" 
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-transparent focus:ring-2 focus:ring-blue-500 outline-none"
              placeholder="••••••••"
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="w-full py-2.5 px-4 mt-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50"
          >
            {loading ? "Please wait..." : isLogin ? "Sign In" : "Register"}
          </button>
        </form>

        <div className="mt-6 text-center text-sm text-zinc-500">
          {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
          <button 
            type="button"
            onClick={() => setIsLogin(!isLogin)}
            className="font-medium text-blue-600 dark:text-blue-400 hover:underline"
          >
            {isLogin ? "Sign up" : "Sign in"}
          </button>
        </div>
        
        <div className="mt-8 text-center">
          <Link href="/" className="text-xs text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200">
            &larr; Return to Home
          </Link>
        </div>

      </div>
    </main>
  );
}

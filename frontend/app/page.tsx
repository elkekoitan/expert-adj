"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type ApiStatus = "loading" | "up" | "down";

export default function LandingPage() {
  const router = useRouter();
  const [status, setStatus] = useState<ApiStatus>("loading");

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/health")
      .then((res) => setStatus(res.ok ? "up" : "down"))
      .catch(() => setStatus("down"));
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-slate-50">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        {/* Animated Background */}
        <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/10 via-blue-500/10 to-purple-500/10 animate-pulse"></div>

        {/* Navigation */}
        <nav className="relative border-b border-slate-800 bg-slate-900/50 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-blue-500 rounded-lg flex items-center justify-center">
                <span className="text-2xl font-bold">M</span>
              </div>
              <span className="text-xl font-bold">MT Expert Optimizer</span>
            </div>
            <div className="flex items-center gap-4">
              <div
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm ${
                  status === "up"
                    ? "bg-emerald-950/50 text-emerald-400 border border-emerald-700"
                    : status === "down"
                      ? "bg-red-950/50 text-red-400 border border-red-700"
                      : "bg-slate-800 text-slate-400"
                }`}
              >
                <div
                  className={`w-2 h-2 rounded-full ${
                    status === "up"
                      ? "bg-emerald-500 animate-pulse"
                      : status === "down"
                        ? "bg-red-500"
                        : "bg-slate-500 animate-pulse"
                  }`}
                ></div>
                <span className="font-semibold">
                  {status === "up"
                    ? "Live"
                    : status === "down"
                      ? "Offline"
                      : "Connecting"}
                </span>
              </div>
              <button
                onClick={() => router.push("/login")}
                className="px-6 py-2 bg-gradient-to-r from-emerald-600 to-blue-600 hover:from-emerald-500 hover:to-blue-500 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105"
              >
                Get Started →
              </button>
            </div>
          </div>
        </nav>

        {/* Hero Content */}
        <div className="relative max-w-7xl mx-auto px-6 py-24">
          <div className="text-center max-w-4xl mx-auto">
            <h1 className="text-6xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-emerald-400 via-blue-400 to-purple-400 bg-clip-text text-transparent animate-gradient">
              AI-Powered Trading
              <br />
              Strategy Optimizer
            </h1>
            <p className="text-xl text-slate-300 mb-8 leading-relaxed">
              Optimize your MT4/MT5 Expert Advisors with cutting-edge AI,
              real-time analytics, and professional-grade backtesting tools.
              Join thousands of traders maximizing their profits.
            </p>
            <div className="flex items-center justify-center gap-4 mb-12">
              <button
                onClick={() => router.push("/login")}
                className="px-8 py-4 bg-gradient-to-r from-emerald-600 to-blue-600 hover:from-emerald-500 hover:to-blue-500 rounded-xl font-bold text-lg transition-all duration-300 transform hover:scale-105 shadow-lg shadow-emerald-500/50"
              >
                Start Free Trial
              </button>
              <button
                onClick={() => router.push("/dashboard")}
                className="px-8 py-4 bg-slate-800 hover:bg-slate-700 rounded-xl font-bold text-lg transition-all duration-300 border border-slate-700"
              >
                View Demo
              </button>
            </div>
            <div className="flex items-center justify-center gap-8 text-sm text-slate-400">
              <div className="flex items-center gap-2">
                <span className="text-emerald-400 text-2xl">✓</span>
                <span>14-day free trial</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-emerald-400 text-2xl">✓</span>
                <span>No credit card required</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-emerald-400 text-2xl">✓</span>
                <span>Cancel anytime</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="max-w-7xl mx-auto px-6 py-24">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">
            Everything You Need to
            <span className="bg-gradient-to-r from-emerald-400 to-blue-400 bg-clip-text text-transparent">
              {" "}
              Dominate Markets
            </span>
          </h2>
          <p className="text-xl text-slate-400">
            Professional trading tools powered by artificial intelligence
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Feature 1 */}
          <div className="group p-8 bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-2xl hover:border-emerald-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-emerald-500/20 transform hover:-translate-y-2">
            <div className="w-16 h-16 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <span className="text-3xl">🤖</span>
            </div>
            <h3 className="text-2xl font-bold mb-3">AI Risk Analysis</h3>
            <p className="text-slate-400 leading-relaxed">
              Advanced machine learning algorithms analyze your trading patterns
              and provide real-time risk scores with actionable recommendations.
            </p>
          </div>

          {/* Feature 2 */}
          <div className="group p-8 bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-2xl hover:border-blue-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-blue-500/20 transform hover:-translate-y-2">
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <span className="text-3xl">📊</span>
            </div>
            <h3 className="text-2xl font-bold mb-3">
              Professional Backtesting
            </h3>
            <p className="text-slate-400 leading-relaxed">
              Test your strategies against historical data with
              institutional-grade accuracy. Monte Carlo simulations included.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="group p-8 bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-2xl hover:border-purple-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-purple-500/20 transform hover:-translate-y-2">
            <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <span className="text-3xl">⚡</span>
            </div>
            <h3 className="text-2xl font-bold mb-3">Real-time Analytics</h3>
            <p className="text-slate-400 leading-relaxed">
              Monitor live positions, track performance metrics, and receive
              instant notifications on market opportunities.
            </p>
          </div>

          {/* Feature 4 */}
          <div className="group p-8 bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-2xl hover:border-amber-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-amber-500/20 transform hover:-translate-y-2">
            <div className="w-16 h-16 bg-gradient-to-br from-amber-500 to-amber-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <span className="text-3xl">🎯</span>
            </div>
            <h3 className="text-2xl font-bold mb-3">Auto-Optimization</h3>
            <p className="text-slate-400 leading-relaxed">
              Let AI find the optimal parameters for your Expert Advisors using
              genetic algorithms and particle swarm optimization.
            </p>
          </div>

          {/* Feature 5 */}
          <div className="group p-8 bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-2xl hover:border-pink-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-pink-500/20 transform hover:-translate-y-2">
            <div className="w-16 h-16 bg-gradient-to-br from-pink-500 to-pink-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <span className="text-3xl">👥</span>
            </div>
            <h3 className="text-2xl font-bold mb-3">Social Trading</h3>
            <p className="text-slate-400 leading-relaxed">
              Connect with top traders, share strategies, and learn from the
              community's best performers in real-time.
            </p>
          </div>

          {/* Feature 6 */}
          <div className="group p-8 bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-2xl hover:border-cyan-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-cyan-500/20 transform hover:-translate-y-2">
            <div className="w-16 h-16 bg-gradient-to-br from-cyan-500 to-cyan-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <span className="text-3xl">🔒</span>
            </div>
            <h3 className="text-2xl font-bold mb-3">Enterprise Security</h3>
            <p className="text-slate-400 leading-relaxed">
              Bank-level encryption, 2FA authentication, and secure API
              connections. Your data is always protected.
            </p>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="bg-gradient-to-r from-emerald-950/50 to-blue-950/50 border-y border-slate-800">
        <div className="max-w-7xl mx-auto px-6 py-16">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-5xl font-bold bg-gradient-to-r from-emerald-400 to-blue-400 bg-clip-text text-transparent mb-2">
                10,000+
              </div>
              <div className="text-slate-400">Active Traders</div>
            </div>
            <div>
              <div className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
                $2.5M+
              </div>
              <div className="text-slate-400">Daily Volume</div>
            </div>
            <div>
              <div className="text-5xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent mb-2">
                99.9%
              </div>
              <div className="text-slate-400">Uptime</div>
            </div>
            <div>
              <div className="text-5xl font-bold bg-gradient-to-r from-pink-400 to-emerald-400 bg-clip-text text-transparent mb-2">
                24/7
              </div>
              <div className="text-slate-400">Support</div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="max-w-4xl mx-auto px-6 py-24 text-center">
        <h2 className="text-5xl font-bold mb-6">
          Ready to{" "}
          <span className="bg-gradient-to-r from-emerald-400 to-blue-400 bg-clip-text text-transparent">
            Transform
          </span>{" "}
          Your Trading?
        </h2>
        <p className="text-xl text-slate-300 mb-12">
          Join thousands of successful traders using AI-powered optimization
        </p>
        <button
          onClick={() => router.push("/login")}
          className="px-12 py-5 bg-gradient-to-r from-emerald-600 to-blue-600 hover:from-emerald-500 hover:to-blue-500 rounded-xl font-bold text-xl transition-all duration-300 transform hover:scale-105 shadow-2xl shadow-emerald-500/50"
        >
          Start Your Free Trial →
        </button>
        <p className="mt-6 text-sm text-slate-400">
          No credit card required • 14-day free trial • Cancel anytime
        </p>
      </div>

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-slate-900/50">
        <div className="max-w-7xl mx-auto px-6 py-12">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-8">
            <div>
              <h4 className="font-bold mb-4">Product</h4>
              <ul className="space-y-2 text-slate-400">
                <li>
                  <Link
                    href="/dashboard"
                    className="hover:text-emerald-400 transition-colors"
                  >
                    Dashboard
                  </Link>
                </li>
                <li>
                  <Link
                    href="/experts"
                    className="hover:text-emerald-400 transition-colors"
                  >
                    Expert Advisors
                  </Link>
                </li>
                <li>
                  <Link
                    href="/backtests"
                    className="hover:text-emerald-400 transition-colors"
                  >
                    Backtesting
                  </Link>
                </li>
                <li>
                  <Link
                    href="/accounts"
                    className="hover:text-emerald-400 transition-colors"
                  >
                    Accounts
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">Company</h4>
              <ul className="space-y-2 text-slate-400">
                <li>
                  <a
                    href="#"
                    className="hover:text-emerald-400 transition-colors"
                  >
                    About
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="hover:text-emerald-400 transition-colors"
                  >
                    Blog
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="hover:text-emerald-400 transition-colors"
                  >
                    Careers
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="hover:text-emerald-400 transition-colors"
                  >
                    Contact
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">Resources</h4>
              <ul className="space-y-2 text-slate-400">
                <li>
                  <a
                    href="#"
                    className="hover:text-emerald-400 transition-colors"
                  >
                    Documentation
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="hover:text-emerald-400 transition-colors"
                  >
                    API Reference
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="hover:text-emerald-400 transition-colors"
                  >
                    Community
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="hover:text-emerald-400 transition-colors"
                  >
                    Support
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">Legal</h4>
              <ul className="space-y-2 text-slate-400">
                <li>
                  <a
                    href="#"
                    className="hover:text-emerald-400 transition-colors"
                  >
                    Privacy
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="hover:text-emerald-400 transition-colors"
                  >
                    Terms
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="hover:text-emerald-400 transition-colors"
                  >
                    Security
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="hover:text-emerald-400 transition-colors"
                  >
                    Compliance
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div className="pt-8 border-t border-slate-800 flex items-center justify-between">
            <p className="text-slate-400 text-sm">
              © 2025 MT Expert Optimizer. All rights reserved.
            </p>
            <div className="flex items-center gap-4">
              <a
                href="#"
                className="text-slate-400 hover:text-emerald-400 transition-colors"
              >
                Twitter
              </a>
              <a
                href="#"
                className="text-slate-400 hover:text-emerald-400 transition-colors"
              >
                LinkedIn
              </a>
              <a
                href="#"
                className="text-slate-400 hover:text-emerald-400 transition-colors"
              >
                GitHub
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

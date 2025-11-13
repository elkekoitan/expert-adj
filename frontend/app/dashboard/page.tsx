"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface AccountMetrics {
  balance: number;
  equity: number;
  margin: number;
  free_margin: number;
  profit: number;
  profit_percent: number;
}

interface Position {
  ticket: string;
  symbol: string;
  type: "BUY" | "SELL";
  volume: number;
  open_price: number;
  current_price: number;
  profit: number;
  profit_percent: number;
  open_time: string;
}

interface AIRiskMetrics {
  risk_score: number;
  risk_level: "LOW" | "MEDIUM" | "HIGH";
  factors: {
    name: string;
    value: number;
    impact: "POSITIVE" | "NEGATIVE";
  }[];
  recommendation: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Data states
  const [metrics, setMetrics] = useState<AccountMetrics | null>(null);
  const [positions, setPositions] = useState<Position[]>([]);
  const [aiRisk, setAIRisk] = useState<AIRiskMetrics | null>(null);
  const [equityHistory, setEquityHistory] = useState<
    { date: string; value: number }[]
  >([]);

  // Fetch data on mount
  useEffect(() => {
    fetchDashboardData();

    // Auto-refresh every 5 seconds
    const interval = setInterval(fetchDashboardData, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      const token =
        typeof window !== "undefined"
          ? window.localStorage.getItem("token")
          : null;
      if (!token) {
        router.push("/login");
        return;
      }

      // Simulate API calls (replace with real API later)
      setMetrics({
        balance: 10000 + Math.random() * 1000,
        equity: 10500 + Math.random() * 500,
        margin: 2000,
        free_margin: 8500,
        profit: 500 + Math.random() * 100,
        profit_percent: 5.5 + Math.random() * 2,
      });

      setPositions([
        {
          ticket: "T001",
          symbol: "EURUSD",
          type: "BUY",
          volume: 0.1,
          open_price: 1.095,
          current_price: 1.0975,
          profit: 25,
          profit_percent: 0.23,
          open_time: new Date(Date.now() - 3600000).toISOString(),
        },
        {
          ticket: "T002",
          symbol: "GBPUSD",
          type: "SELL",
          volume: 0.2,
          open_price: 1.265,
          current_price: 1.2625,
          profit: 50,
          profit_percent: 0.2,
          open_time: new Date(Date.now() - 7200000).toISOString(),
        },
      ]);

      setAIRisk({
        risk_score: 35 + Math.random() * 10,
        risk_level: "MEDIUM",
        factors: [
          { name: "Drawdown Risk", value: 25, impact: "NEGATIVE" },
          { name: "Position Diversification", value: 75, impact: "POSITIVE" },
          { name: "Volatility Exposure", value: 45, impact: "NEGATIVE" },
          { name: "Win Rate Trend", value: 65, impact: "POSITIVE" },
        ],
        recommendation:
          "Consider reducing position sizes during high volatility periods",
      });

      // Generate equity history
      const history = [];
      for (let i = 30; i >= 0; i--) {
        history.push({
          date: new Date(Date.now() - i * 24 * 3600000)
            .toISOString()
            .split("T")[0],
          value: 10000 + (30 - i) * 20 + Math.random() * 100,
        });
      }
      setEquityHistory(history);

      setLoading(false);
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  };

  const getRiskColor = (score: number) => {
    if (score < 30)
      return "text-emerald-400 bg-emerald-950/50 border-emerald-700";
    if (score < 60) return "text-amber-400 bg-amber-950/50 border-amber-700";
    return "text-red-400 bg-red-950/50 border-red-700";
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-slate-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-slate-400">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-slate-50">
      {/* Header */}
      <div className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-emerald-400 to-blue-500 bg-clip-text text-transparent">
                Live Trading Dashboard
              </h1>
              <p className="text-slate-400 text-sm mt-1">
                Real-time AI-powered trading analytics
              </p>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 px-4 py-2 bg-emerald-950/50 border border-emerald-700 rounded-lg">
                <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-semibold text-emerald-400">
                  Live
                </span>
              </div>
              <button
                onClick={() => router.push("/")}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors"
              >
                ← Back to Home
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Error Alert */}
        {error && (
          <div className="mb-6 p-4 bg-red-950/50 border border-red-700 rounded-lg text-red-300">
            {error}
          </div>
        )}

        {/* Account Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-xl p-6 hover:border-emerald-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-emerald-500/20">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400 text-sm font-semibold">
                Balance
              </span>
              <span className="text-2xl">💰</span>
            </div>
            <p className="text-3xl font-bold text-slate-50">
              ${metrics?.balance.toFixed(2)}
            </p>
            <p className="text-xs text-slate-500 mt-1">Account balance</p>
          </div>

          <div className="bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-xl p-6 hover:border-blue-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/20">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400 text-sm font-semibold">
                Equity
              </span>
              <span className="text-2xl">📊</span>
            </div>
            <p className="text-3xl font-bold text-blue-400">
              ${metrics?.equity.toFixed(2)}
            </p>
            <p className="text-xs text-slate-500 mt-1">Current equity value</p>
          </div>

          <div className="bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-xl p-6 hover:border-emerald-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-emerald-500/20">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400 text-sm font-semibold">
                Profit
              </span>
              <span className="text-2xl">📈</span>
            </div>
            <p className="text-3xl font-bold text-emerald-400">
              +${metrics?.profit.toFixed(2)}
            </p>
            <p className="text-xs text-emerald-500 mt-1">
              +{metrics?.profit_percent.toFixed(2)}%
            </p>
          </div>

          <div className="bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-xl p-6 hover:border-purple-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-purple-500/20">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400 text-sm font-semibold">
                Free Margin
              </span>
              <span className="text-2xl">💎</span>
            </div>
            <p className="text-3xl font-bold text-purple-400">
              ${metrics?.free_margin.toFixed(2)}
            </p>
            <p className="text-xs text-slate-500 mt-1">Available for trading</p>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - AI Risk Analysis + Equity Chart */}
          <div className="lg:col-span-2 space-y-6">
            {/* AI Risk Meter */}
            <div className="bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-xl p-6">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-purple-500/20 rounded-lg flex items-center justify-center">
                    <span className="text-2xl">🤖</span>
                  </div>
                  <div>
                    <h2 className="text-xl font-bold">AI Risk Analysis</h2>
                    <p className="text-sm text-slate-400">
                      Real-time ML-powered risk assessment
                    </p>
                  </div>
                </div>
                <div
                  className={`px-4 py-2 rounded-lg border ${getRiskColor(aiRisk?.risk_score || 0)}`}
                >
                  <span className="font-bold">{aiRisk?.risk_level}</span>
                </div>
              </div>

              {/* Risk Score Gauge */}
              <div className="mb-6">
                <div className="flex justify-between mb-2">
                  <span className="text-sm text-slate-400">Risk Score</span>
                  <span className="text-lg font-bold">
                    {aiRisk?.risk_score.toFixed(1)}/100
                  </span>
                </div>
                <div className="w-full h-3 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-emerald-500 via-amber-500 to-red-500 transition-all duration-500"
                    style={{ width: `${aiRisk?.risk_score}%` }}
                  ></div>
                </div>
                <div className="flex justify-between mt-1 text-xs text-slate-500">
                  <span>Low Risk</span>
                  <span>High Risk</span>
                </div>
              </div>

              {/* Risk Factors */}
              <div className="space-y-3">
                <h3 className="text-sm font-semibold text-slate-300 mb-3">
                  Risk Factors
                </h3>
                {aiRisk?.factors.map((factor, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg"
                  >
                    <span className="text-sm text-slate-300">
                      {factor.name}
                    </span>
                    <div className="flex items-center gap-3">
                      <div className="w-24 h-2 bg-slate-700 rounded-full overflow-hidden">
                        <div
                          className={`h-full ${factor.impact === "POSITIVE" ? "bg-emerald-500" : "bg-red-500"}`}
                          style={{ width: `${factor.value}%` }}
                        ></div>
                      </div>
                      <span
                        className={`text-sm font-semibold w-12 text-right ${
                          factor.impact === "POSITIVE"
                            ? "text-emerald-400"
                            : "text-red-400"
                        }`}
                      >
                        {factor.value}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>

              {/* AI Recommendation */}
              {aiRisk?.recommendation && (
                <div className="mt-6 p-4 bg-blue-950/30 border border-blue-700/50 rounded-lg">
                  <div className="flex items-start gap-3">
                    <span className="text-2xl">💡</span>
                    <div>
                      <p className="text-sm font-semibold text-blue-300 mb-1">
                        AI Recommendation
                      </p>
                      <p className="text-sm text-slate-300">
                        {aiRisk.recommendation}
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Equity Chart */}
            <div className="bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-xl p-6">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <span>📊</span>
                <span>Equity Performance (30 Days)</span>
              </h2>
              <div className="h-64 flex items-end justify-between gap-1">
                {equityHistory.slice(-15).map((point, idx) => (
                  <div key={idx} className="flex-1 flex flex-col items-center">
                    <div
                      className="w-full bg-gradient-to-t from-emerald-500 to-emerald-400 rounded-t hover:from-emerald-400 hover:to-emerald-300 transition-all duration-300 cursor-pointer"
                      style={{
                        height: `${(point.value - 10000) / 10}%`,
                        minHeight: "4px",
                      }}
                      title={`${point.date}: $${point.value.toFixed(2)}`}
                    ></div>
                  </div>
                ))}
              </div>
              <div className="flex justify-between mt-4 text-xs text-slate-500">
                <span>{equityHistory[equityHistory.length - 15]?.date}</span>
                <span>{equityHistory[equityHistory.length - 1]?.date}</span>
              </div>
            </div>
          </div>

          {/* Right Column - Live Positions */}
          <div className="space-y-6">
            <div className="bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-xl p-6">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <span>🔥</span>
                <span>Live Positions</span>
                <span className="ml-auto text-sm font-normal text-slate-400">
                  {positions.length} active
                </span>
              </h2>

              {positions.length === 0 ? (
                <div className="text-center py-8">
                  <p className="text-slate-400 mb-2">No open positions</p>
                  <p className="text-sm text-slate-500">
                    Your trades will appear here
                  </p>
                </div>
              ) : (
                <div className="space-y-3">
                  {positions.map((pos) => (
                    <div
                      key={pos.ticket}
                      className="p-4 bg-slate-800/50 border border-slate-700 rounded-lg hover:border-emerald-500/50 transition-all duration-300"
                    >
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-2">
                          <span className="text-lg font-bold">
                            {pos.symbol}
                          </span>
                          <span
                            className={`px-2 py-0.5 rounded text-xs font-semibold ${
                              pos.type === "BUY"
                                ? "bg-emerald-500/20 text-emerald-400"
                                : "bg-red-500/20 text-red-400"
                            }`}
                          >
                            {pos.type}
                          </span>
                        </div>
                        <span
                          className={`text-lg font-bold ${
                            pos.profit >= 0
                              ? "text-emerald-400"
                              : "text-red-400"
                          }`}
                        >
                          {pos.profit >= 0 ? "+" : ""}${pos.profit.toFixed(2)}
                        </span>
                      </div>

                      <div className="grid grid-cols-2 gap-2 text-sm">
                        <div>
                          <span className="text-slate-500">Volume:</span>
                          <span className="ml-2 text-slate-300 font-semibold">
                            {pos.volume}
                          </span>
                        </div>
                        <div>
                          <span className="text-slate-500">P/L%:</span>
                          <span
                            className={`ml-2 font-semibold ${
                              pos.profit_percent >= 0
                                ? "text-emerald-400"
                                : "text-red-400"
                            }`}
                          >
                            {pos.profit_percent >= 0 ? "+" : ""}
                            {pos.profit_percent.toFixed(2)}%
                          </span>
                        </div>
                        <div>
                          <span className="text-slate-500">Open:</span>
                          <span className="ml-2 text-slate-300">
                            {pos.open_price.toFixed(5)}
                          </span>
                        </div>
                        <div>
                          <span className="text-slate-500">Current:</span>
                          <span className="ml-2 text-slate-300">
                            {pos.current_price.toFixed(5)}
                          </span>
                        </div>
                      </div>

                      <div className="mt-3 pt-3 border-t border-slate-700">
                        <span className="text-xs text-slate-500">
                          Opened: {new Date(pos.open_time).toLocaleString()}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              <button className="w-full mt-4 px-4 py-3 bg-emerald-600 hover:bg-emerald-500 rounded-lg font-semibold transition-colors">
                View All Trades →
              </button>
            </div>

            {/* Quick Actions */}
            <div className="bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-xl p-6">
              <h3 className="text-lg font-bold mb-4">Quick Actions</h3>
              <div className="space-y-2">
                <button
                  onClick={() => router.push("/accounts")}
                  className="w-full px-4 py-3 bg-blue-600 hover:bg-blue-500 rounded-lg text-left transition-colors flex items-center justify-between"
                >
                  <span>💼 Manage Accounts</span>
                  <span>→</span>
                </button>
                <button
                  onClick={() => router.push("/experts")}
                  className="w-full px-4 py-3 bg-purple-600 hover:bg-purple-500 rounded-lg text-left transition-colors flex items-center justify-between"
                >
                  <span>📚 Expert Advisors</span>
                  <span>→</span>
                </button>
                <button
                  onClick={() => router.push("/backtests")}
                  className="w-full px-4 py-3 bg-amber-600 hover:bg-amber-500 rounded-lg text-left transition-colors flex items-center justify-between"
                >
                  <span>📊 Run Backtest</span>
                  <span>→</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Performance Statistics */}
        <div className="mt-8 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-4 bg-slate-900/50 border border-slate-800 rounded-lg">
            <p className="text-sm text-slate-400 mb-1">Win Rate</p>
            <p className="text-2xl font-bold text-emerald-400">68.5%</p>
          </div>
          <div className="p-4 bg-slate-900/50 border border-slate-800 rounded-lg">
            <p className="text-sm text-slate-400 mb-1">Total Trades</p>
            <p className="text-2xl font-bold">247</p>
          </div>
          <div className="p-4 bg-slate-900/50 border border-slate-800 rounded-lg">
            <p className="text-sm text-slate-400 mb-1">Avg Profit</p>
            <p className="text-2xl font-bold text-emerald-400">$125</p>
          </div>
          <div className="p-4 bg-slate-900/50 border border-slate-800 rounded-lg">
            <p className="text-sm text-slate-400 mb-1">Max Drawdown</p>
            <p className="text-2xl font-bold text-red-400">-8.2%</p>
          </div>
        </div>
      </div>
    </div>
  );
}

"use client";

import { useEffect, useState } from "react";

type BacktestStatus = "queued" | "running" | "completed" | "failed";

interface BacktestRun {
  id: string;
  preset_id: string | null;
  preset_name?: string;
  symbol: string;
  timeframe: string;
  status: BacktestStatus;
  // Backend metrics alanı; mock slice'ta buradan da gelebilir
  metrics?: {
    net_profit?: number;
    max_drawdown?: number;
    total_trades?: number;
    [key: string]: any;
  } | null;
  started_at?: string | null;
  completed_at?: string | null;
  initial_balance?: number | null;
  final_balance?: number | null;
  net_profit?: number | null;
  max_drawdown?: number | null;
  total_trades?: number | null;
}

interface StrategyPreset {
  id: string;
  name: string;
  slug: string;
  symbol: string;
  timeframe: string;
  status: string;
}

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export default function BacktestsPage() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [backtests, setBacktests] = useState<BacktestRun[]>([]);
  const [presets, setPresets] = useState<StrategyPreset[]>([]);
  const [selectedPreset, setSelectedPreset] = useState<string>("");
  const [creating, setCreating] = useState(false);

  const getAuthHeaders = (): Record<string, string> => {
    if (typeof window === "undefined") return {};
    const token = window.localStorage.getItem("token");
    return token ? { Authorization: `Bearer ${token}` } : {};
  };

  // Backtest ve presetleri yükle (auth zorunlu)
  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        setError(null);

        const headers: Record<string, string> = {
          "Content-Type": "application/json",
          ...getAuthHeaders(),
        };

        const [btRes, prRes] = await Promise.all([
          fetch(`${API_BASE}/backtests`, { headers }),
          fetch(`${API_BASE}/strategy-presets`, { headers }),
        ]);

        if (btRes.status === 401 || btRes.status === 403) {
          if (typeof window !== "undefined") {
            window.location.href = "/login";
          }
          return;
        }

        if (!btRes.ok) {
          throw new Error("Backtests fetch failed");
        }
        if (!prRes.ok) {
          throw new Error("Presets fetch failed");
        }

        const btData = await btRes.json();
        const prData = await prRes.json();

        setBacktests(btData || []);
        setPresets(prData || []);
      } catch (e: any) {
        console.error(e);
        setError(
          "Veriler alınamadı. Login durumu veya backend API/DB durumunu kontrol et.",
        );
      } finally {
        setLoading(false);
      }
    };

    // Token yoksa direkt login'e at
    if (typeof window !== "undefined") {
      const token = window.localStorage.getItem("token");
      if (!token) {
        window.location.href = "/login";
        return;
      }
    }

    load();
  }, []);

  const findPresetName = (preset_id: string | null) => {
    if (!preset_id) return "";
    const p = presets.find((p) => p.id === preset_id);
    return p ? p.name : "";
  };

  const handleCreateForPreset = async () => {
    if (!selectedPreset) return;
    try {
      setCreating(true);
      setError(null);

      const headers = {
        "Content-Type": "application/json",
        ...getAuthHeaders(),
      };

      const res = await fetch(
        `${API_BASE}/strategy-presets/${selectedPreset}/backtests`,
        {
          method: "POST",
          headers,
          body: JSON.stringify({}),
        },
      );

      if (res.status === 401 || res.status === 403) {
        if (typeof window !== "undefined") {
          window.location.href = "/login";
        }
        return;
      }

      if (!res.ok) {
        const detail = await res.text();
        throw new Error(detail || "Backtest oluşturulamadı");
      }

      const created = await res.json();
      setBacktests((prev) => [created, ...prev]);
    } catch (e: any) {
      console.error(e);
      setError(e.message || "Backtest oluşturulamadı");
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 p-8">
      <div className="max-w-6xl mx-auto space-y-6">
        <header className="flex flex-col gap-2">
          <h1 className="text-3xl font-bold">Backtest Raporları</h1>
          <p className="text-slate-400 text-sm">
            StrategyPreset tablosundaki ayar setleri ile oluşturulan backtest
            sonuçlarını burada gör.
          </p>
        </header>

        {/* Preset seç ve backtest oluştur */}
        <section className="border border-slate-800 bg-slate-900/40 rounded-xl p-4 flex flex-col md:flex-row gap-3 items-start md:items-end">
          <div className="flex-1">
            <label className="block text-xs text-slate-500 mb-1">
              NewBorn / diğer presetler
            </label>
            <select
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500"
              value={selectedPreset}
              onChange={(e) => setSelectedPreset(e.target.value)}
            >
              <option value="">
                Preset seç (örn: NewBornDongu_XAUUSD_M15_CORE_v1)
              </option>
              {presets.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name} ({p.symbol} {p.timeframe})
                </option>
              ))}
            </select>
          </div>
          <button
            onClick={handleCreateForPreset}
            disabled={!selectedPreset || creating}
            className="px-4 py-2 rounded-lg text-sm font-semibold bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-700 disabled:text-slate-500 transition-colors"
          >
            {creating
              ? "Oluşturuluyor..."
              : "Seçili preset ile backtest oluştur"}
          </button>
        </section>

        {error && (
          <div className="border border-red-500/40 bg-red-950/40 text-red-300 text-sm px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        <section className="border border-slate-800 bg-slate-900/40 rounded-xl">
          <div className="px-4 py-3 border-b border-slate-800 flex items-center justify-between">
            <h2 className="text-lg font-semibold">Backtestler</h2>
            {loading && (
              <span className="text-xs text-slate-400">Yükleniyor...</span>
            )}
          </div>
          <div className="overflow-x-auto">
            {backtests.length === 0 && !loading ? (
              <div className="px-4 py-10 text-center text-slate-500 text-sm">
                Henüz backtest yok. Üstten bir preset seçip backtest oluştur.
              </div>
            ) : (
              <table className="w-full text-sm">
                <thead className="bg-slate-900/70">
                  <tr>
                    <th className="px-4 py-2 text-left text-slate-500 font-medium">
                      Preset
                    </th>
                    <th className="px-4 py-2 text-left text-slate-500 font-medium">
                      Sembol / TF
                    </th>
                    <th className="px-4 py-2 text-left text-slate-500 font-medium">
                      Durum
                    </th>
                    <th className="px-4 py-2 text-left text-slate-500 font-medium">
                      Net Kar
                    </th>
                    <th className="px-4 py-2 text-left text-slate-500 font-medium">
                      Max DD
                    </th>
                    <th className="px-4 py-2 text-left text-slate-500 font-medium">
                      Toplam İşlem
                    </th>
                    <th className="px-4 py-2 text-left text-slate-500 font-medium">
                      Başlangıç
                    </th>
                    <th className="px-4 py-2 text-left text-slate-500 font-medium">
                      Bitiş
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {backtests.map((bt) => {
                    const presetName =
                      bt.preset_name || findPresetName(bt.preset_id);
                    return (
                      <tr
                        key={bt.id}
                        className="border-t border-slate-800 hover:bg-slate-900/70"
                      >
                        <td className="px-4 py-2">
                          <div className="flex flex-col">
                            <span className="font-semibold text-slate-100">
                              {presetName || "N/A"}
                            </span>
                            <span className="text-[10px] text-slate-500">
                              {bt.id}
                            </span>
                          </div>
                        </td>
                        <td className="px-4 py-2 text-slate-300">
                          {bt.symbol} {bt.timeframe}
                        </td>
                        <td className="px-4 py-2">
                          <span
                            className={
                              "px-2 py-1 rounded-full text-[10px] uppercase " +
                              (bt.status === "completed"
                                ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/30"
                                : bt.status === "running"
                                  ? "bg-blue-500/10 text-blue-400 border border-blue-500/30"
                                  : bt.status === "failed"
                                    ? "bg-red-500/10 text-red-400 border border-red-500/30"
                                    : "bg-slate-700/60 text-slate-300 border border-slate-600")
                            }
                          >
                            {bt.status}
                          </span>
                        </td>
                        <td className="px-4 py-2">
                          {bt.net_profit != null ||
                          bt.metrics?.net_profit != null ? (
                            <span
                              className={
                                (bt.net_profit ??
                                  bt.metrics?.net_profit ??
                                  0) >= 0
                                  ? "text-emerald-400"
                                  : "text-red-400"
                              }
                            >
                              $
                              {(
                                bt.net_profit ??
                                bt.metrics?.net_profit ??
                                0
                              ).toFixed(2)}
                            </span>
                          ) : (
                            <span className="text-slate-500">-</span>
                          )}
                        </td>
                        <td className="px-4 py-2">
                          {bt.max_drawdown != null ||
                          bt.metrics?.max_drawdown != null ? (
                            <span className="text-slate-300">
                              $
                              {(
                                bt.max_drawdown ??
                                bt.metrics?.max_drawdown ??
                                0
                              ).toFixed(2)}
                            </span>
                          ) : (
                            <span className="text-slate-500">-</span>
                          )}
                        </td>
                        <td className="px-4 py-2">
                          {bt.total_trades != null ||
                          bt.metrics?.total_trades != null ? (
                            <span className="text-slate-300">
                              {bt.total_trades ?? bt.metrics?.total_trades ?? 0}
                            </span>
                          ) : (
                            <span className="text-slate-500">-</span>
                          )}
                        </td>
                        <td className="px-4 py-2 text-slate-500 text-[10px]">
                          {bt.started_at || "-"}
                        </td>
                        <td className="px-4 py-2 text-slate-500 text-[10px]">
                          {bt.completed_at || "-"}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            )}
          </div>
        </section>
      </div>
    </div>
  );
}

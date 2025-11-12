'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'

type ApiStatus = 'loading' | 'up' | 'down'

async function checkApi(): Promise<ApiStatus> {
  try {
    const res = await fetch('http://localhost:8000/api/v1/health')
    if (!res.ok) return 'down'
    return 'up'
  } catch {
    return 'down'
  }
}

export default function Home() {
  const [status, setStatus] = useState<ApiStatus>('loading')

  useEffect(() => {
    checkApi().then(setStatus)
  }, [])

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-6xl mx-auto px-6 py-16">
        <header className="mb-12 flex flex-col gap-4">
          <h1 className="text-4xl md:text-5xl font-bold">
            MT Expert Optimizer
          </h1>
          <p className="text-slate-400 text-lg max-w-2xl">
            NewBornDongu ve diğer EA'ler için backtest, preset yönetimi ve optimizasyonu tek panelden yönet.
          </p>
          <div className="flex items-center gap-3 text-sm">
            <div
              className={`
                h-2 w-2 rounded-full
                ${status === 'loading' ? 'bg-yellow-400 animate-pulse' : ''}
                ${status === 'up' ? 'bg-emerald-400' : ''}
                ${status === 'down' ? 'bg-red-500' : ''}
              `}
            />
            <span className="text-slate-400">
              API:{' '}
              {status === 'loading' && 'kontrol ediliyor...'}
              {status === 'up' && 'bağlandı'}
              {status === 'down' && 'erişilemiyor'}
            </span>
          </div>
        </header>

        <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <Link
            href="/experts"
            className="group border border-slate-800 bg-slate-900/40 rounded-xl p-6 hover:border-emerald-400/70 hover:bg-slate-900 transition-colors"
          >
            <h2 className="text-xl font-semibold mb-2">📚 EA / Preset Yönetimi</h2>
            <p className="text-slate-400 mb-3">
              NewBornDongu_ParalelRobotlar dahil EA'leri yükle, parametreleri çıkar ve preset setleri oluştur.
            </p>
            <span className="text-emerald-400 text-sm group-hover:underline">
              Preset ekranına git
            </span>
          </Link>

          <Link
            href="/backtests"
            className="group border border-slate-800 bg-slate-900/40 rounded-xl p-6 hover:border-blue-400/70 hover:bg-slate-900 transition-colors"
          >
            <h2 className="text-xl font-semibold mb-2">📊 Backtest Raporları</h2>
            <p className="text-slate-400 mb-3">
              Farklı ayar setleri ile çalıştırılmış backtest sonuçlarını kıyasla, en stabil kombinasyonu seç.
            </p>
            <span className="text-blue-400 text-sm group-hover:underline">
              Raporları görüntüle
            </span>
          </Link>

          <Link
            href="/dashboard"
            className="group border border-slate-800 bg-slate-900/40 rounded-xl p-6 hover:border-purple-400/70 hover:bg-slate-900 transition-colors"
          >
            <h2 className="text-xl font-semibold mb-2">📡 Canlı Hesap İzleme</h2>
            <p className="text-slate-400 mb-3">
              Demo hesabını WebSocket ile bağla, pozisyon ve PnL'i canlı takip et.
            </p>
            <span className="text-purple-400 text-sm group-hover:underline">
              Dashboard'a git
            </span>
          </Link>
        </section>

        <section className="border border-slate-800 bg-slate-900/40 rounded-xl p-6">
          <h3 className="text-lg font-semibold mb-2">NewBornDongu Demo Akışı</h3>
          <ol className="list-decimal list-inside text-sm text-slate-300 space-y-1">
            <li>NewBornDongu_ParalelRobotlar.mq4 dosyasını MetaTrader 4 terminaline ekle.</li>
            <li>Demo hesap bilgilerini kullanarak terminali bağla.</li>
            <li>/experts sayfasından EA/preset ayarlarını yönet.</li>
            <li>/backtests sayfasından backtestleri ve sonuç raporlarını görüntüle.</li>
          </ol>
        </section>
      </div>
    </main>
  )
}

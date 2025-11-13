'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

interface MTAccount {
  id: string
  account_id: string
  login: string
  server: string
  is_demo: boolean
  status: string
  balance?: number
  equity?: number
  created_at: string
}

export default function AccountsPage() {
  const router = useRouter()
  const [accounts, setAccounts] = useState<MTAccount[]>([])
  const [loading, setLoading] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  // Form state
  const [formData, setFormData] = useState({
    login: '',
    password: '',
    server: 'MetaQuotes-Demo',
    is_demo: true,
  })

  // Fetch accounts on mount
  useEffect(() => {
    fetchAccounts()
  }, [])

  const fetchAccounts = async () => {
    try {
      const token = typeof window !== 'undefined' ? window.localStorage.getItem('token') : null
      if (!token) {
        router.push('/login')
        return
      }

      const res = await fetch(`${API_BASE}/accounts`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })

      if (!res.ok) throw new Error('Hesapları yükleme başarısız')
      const data = await res.json()
      setAccounts(Array.isArray(data) ? data : data.accounts || [])
    } catch (err: any) {
      setError(err.message)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setSuccess(null)

    try {
      const token = typeof window !== 'undefined' ? window.localStorage.getItem('token') : null
      if (!token) {
        router.push('/login')
        return
      }

      const res = await fetch(`${API_BASE}/accounts`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (!res.ok) {
        const data = await res.json().catch(() => null)
        throw new Error(data?.detail || 'Hesap ekleme başarısız')
      }

      const newAccount = await res.json()
      setAccounts([...accounts, newAccount])
      setFormData({ login: '', password: '', server: 'MetaQuotes-Demo', is_demo: true })
      setShowForm(false)
      setSuccess('MT4 hesabı başarıyla eklendi!')

      // Auto-hide success message
      setTimeout(() => setSuccess(null), 3000)
    } catch (err: any) {
      setError(err.message || 'Bir hata oluştu')
    } finally {
      setLoading(false)
    }
  }

  const handleTestConnection = async (accountId: string) => {
    setLoading(true)
    setError(null)

    try {
      const token = typeof window !== 'undefined' ? window.localStorage.getItem('token') : null
      if (!token) {
        router.push('/login')
        return
      }

      const res = await fetch(`${API_BASE}/accounts/${accountId}/test-connection`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })

      if (!res.ok) throw new Error('Bağlantı testi başarısız')

      const result = await res.json()
      setSuccess(`Bağlantı başarılı! Balance: ${result.balance}`)
      setTimeout(() => setSuccess(null), 3000)

      // Refresh accounts
      fetchAccounts()
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold">MT4/MT5 Hesapları</h1>
            <p className="text-slate-400 mt-2">Trading hesaplarınızı yönetin ve bağlayın</p>
          </div>
          <button
            onClick={() => setShowForm(!showForm)}
            className="px-6 py-3 bg-emerald-600 hover:bg-emerald-500 rounded-lg font-semibold transition-colors"
          >
            {showForm ? 'İptal Et' : '+ Yeni Hesap Ekle'}
          </button>
        </div>

        {/* Messages */}
        {error && (
          <div className="mb-4 p-4 bg-red-950/50 border border-red-700 rounded-lg text-red-300">
            {error}
          </div>
        )}
        {success && (
          <div className="mb-4 p-4 bg-emerald-950/50 border border-emerald-700 rounded-lg text-emerald-300">
            {success}
          </div>
        )}

        {/* Form */}
        {showForm && (
          <div className="mb-8 bg-slate-900/60 border border-slate-800 rounded-xl p-6">
            <h2 className="text-2xl font-bold mb-6">Yeni MT4 Hesabı Ekle</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold mb-2">MT4 Login Numarası</label>
                  <input
                    type="text"
                    value={formData.login}
                    onChange={e => setFormData({ ...formData, login: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-emerald-500"
                    placeholder="123456"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold mb-2">Şifre</label>
                  <input
                    type="password"
                    value={formData.password}
                    onChange={e => setFormData({ ...formData, password: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-emerald-500"
                    placeholder="MT4 şifresi"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold mb-2">Server</label>
                  <select
                    value={formData.server}
                    onChange={e => setFormData({ ...formData, server: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-emerald-500"
                  >
                    <option>MetaQuotes-Demo</option>
                    <option>MetaQuotes-Live</option>
                    <option>Tallinex-Demo</option>
                    <option>Tallinex-Live</option>
                  </select>
                </div>
                <div className="flex items-end">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.is_demo}
                      onChange={e => setFormData({ ...formData, is_demo: e.target.checked })}
                      className="w-4 h-4 rounded"
                    />
                    <span className="ml-2 text-sm">Demo Hesap</span>
                  </label>
                </div>
              </div>
              <div className="flex gap-3 pt-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 px-6 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-700 rounded-lg font-semibold transition-colors"
                >
                  {loading ? 'Ekleniyor...' : 'Hesap Ekle'}
                </button>
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="px-6 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg font-semibold transition-colors"
                >
                  İptal Et
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Accounts List */}
        <div className="space-y-4">
          {accounts.length === 0 ? (
            <div className="text-center py-12 bg-slate-900/60 border border-slate-800 rounded-xl">
              <p className="text-slate-400 mb-4">Henüz MT4 hesabı eklenmemiş</p>
              <button
                onClick={() => setShowForm(true)}
                className="px-6 py-2 bg-emerald-600 hover:bg-emerald-500 rounded-lg font-semibold"
              >
                İlk Hesabı Ekle
              </button>
            </div>
          ) : (
            accounts.map(account => (
              <div
                key={account.id}
                className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 hover:border-slate-700 transition-colors"
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-bold">{account.login}</h3>
                    <p className="text-slate-400 text-sm mt-1">
                      {account.server} · {account.is_demo ? '📊 Demo' : '💰 Live'}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-2xl font-bold text-emerald-400">
                      ${account.balance?.toFixed(2) || '---'}
                    </p>
                    <p className="text-sm text-slate-400">Balance</p>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4 mb-4 py-4 border-y border-slate-800">
                  <div>
                    <p className="text-sm text-slate-400">Equity</p>
                    <p className="text-lg font-semibold">${account.equity?.toFixed(2) || '---'}</p>
                  </div>
                  <div>
                    <p className="text-sm text-slate-400">Status</p>
                    <p className={`text-lg font-semibold ${
                      account.status === 'connected' ? 'text-emerald-400' : 'text-slate-400'
                    }`}>
                      {account.status === 'connected' ? '🟢 Aktif' : '⚫ Bekleme'}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-slate-400">Eklenme Tarihi</p>
                    <p className="text-lg font-semibold">
                      {new Date(account.created_at).toLocaleDateString('tr-TR')}
                    </p>
                  </div>
                </div>

                <div className="flex gap-3">
                  <button
                    onClick={() => handleTestConnection(account.id)}
                    disabled={loading}
                    className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 rounded-lg text-sm font-semibold transition-colors"
                  >
                    {loading ? 'Test ediliyor...' : '🔗 Bağlantıyı Test Et'}
                  </button>
                  <button
                    className="flex-1 px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-sm font-semibold transition-colors"
                  >
                    ⚙️ Ayarlar
                  </button>
                  <button
                    className="flex-1 px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-sm font-semibold transition-colors"
                  >
                    📊 Backtest
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

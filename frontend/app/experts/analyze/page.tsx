'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

interface AnalysisResult {
  status: string
  filename: string
  file_size: number
  metadata: {
    name: string
    version: string
    build: number
    copyright: string
    platform: string
    file_size: number
    file_hash: string
  }
  parameters: Array<{
    name: string
    type: string
    default_value: any
    is_optimizable: boolean
    description: string
  }>
  trading_logic: {
    indicators: string[]
    uses_stop_loss: boolean
    uses_take_profit: boolean
    uses_trailing_stop: boolean
    uses_martingale: boolean
    uses_grid: boolean
    timeframes: string[]
  }
  risk_assessment: {
    score: number
    level: string
    factors: Array<{
      factor: string
      severity: string
      description: string
    }>
  }
  recommendations: string[]
}

export default function EAAnalyzerPage() {
  const router = useRouter()
  const [file, setFile] = useState<File | null>(null)
  const [analyzing, setAnalyzing] = useState(false)
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      // Validate extension
      const ext = selectedFile.name.split('.').pop()?.toLowerCase()
      if (!['ex4', 'ex5', 'mq4', 'mq5'].includes(ext || '')) {
        setError('Invalid file type. Please upload .ex4, .ex5, .mq4, or .mq5 files.')
        return
      }
      setFile(selectedFile)
      setError(null)
      setAnalysis(null)
    }
  }

  const handleAnalyze = async () => {
    if (!file) return

    setAnalyzing(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('http://localhost:8000/api/v1/expert-advisors/analyze', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.statusText}`)
      }

      const result = await response.json()
      setAnalysis(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed')
    } finally {
      setAnalyzing(false)
    }
  }

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'LOW':
        return 'text-emerald-500'
      case 'MEDIUM':
        return 'text-amber-500'
      case 'HIGH':
        return 'text-red-500'
      default:
        return 'text-gray-500'
    }
  }

  const getSeverityBadge = (severity: string) => {
    const colors = {
      low: 'bg-blue-500/20 text-blue-400',
      medium: 'bg-amber-500/20 text-amber-400',
      high: 'bg-red-500/20 text-red-400',
    }
    return colors[severity as keyof typeof colors] || colors.medium
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
              EA Analyzer
            </h1>
            <p className="text-slate-400 mt-2">
              Advanced binary analysis for MetaTrader Expert Advisors
            </p>
          </div>
          <button
            onClick={() => router.push('/experts')}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors"
          >
            ← Back to Experts
          </button>
        </div>

        {/* Upload Section */}
        <div className="bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-xl p-8">
          <h2 className="text-2xl font-semibold mb-6">Upload EA File</h2>

          <div className="space-y-4">
            <div className="border-2 border-dashed border-slate-600 rounded-lg p-12 text-center hover:border-blue-500 transition-colors">
              <input
                type="file"
                accept=".ex4,.ex5,.mq4,.mq5"
                onChange={handleFileSelect}
                className="hidden"
                id="ea-file-input"
              />
              <label htmlFor="ea-file-input" className="cursor-pointer">
                <div className="text-6xl mb-4">📊</div>
                <p className="text-xl font-semibold mb-2">
                  {file ? file.name : 'Choose EA file'}
                </p>
                <p className="text-slate-400">
                  Supports .ex4, .ex5, .mq4, .mq5 files
                </p>
                {file && (
                  <p className="text-sm text-slate-500 mt-2">
                    Size: {(file.size / 1024).toFixed(2)} KB
                  </p>
                )}
              </label>
            </div>

            {error && (
              <div className="bg-red-500/10 border border-red-500/50 rounded-lg p-4 text-red-400">
                {error}
              </div>
            )}

            <button
              onClick={handleAnalyze}
              disabled={!file || analyzing}
              className="w-full py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 disabled:from-slate-700 disabled:to-slate-700 disabled:cursor-not-allowed rounded-lg font-semibold text-lg transition-all"
            >
              {analyzing ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="animate-spin">⚙️</span>
                  Analyzing...
                </span>
              ) : (
                'Analyze EA'
              )}
            </button>
          </div>
        </div>

        {/* Analysis Results */}
        {analysis && (
          <div className="space-y-6">
            {/* Metadata */}
            <div className="bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-xl p-6">
              <h2 className="text-2xl font-semibold mb-4">EA Metadata</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div>
                  <p className="text-slate-400 text-sm">Name</p>
                  <p className="text-lg font-semibold">{analysis.metadata.name}</p>
                </div>
                <div>
                  <p className="text-slate-400 text-sm">Version</p>
                  <p className="text-lg font-semibold">{analysis.metadata.version}</p>
                </div>
                <div>
                  <p className="text-slate-400 text-sm">Platform</p>
                  <p className="text-lg font-semibold">{analysis.metadata.platform}</p>
                </div>
                <div>
                  <p className="text-slate-400 text-sm">Build</p>
                  <p className="text-lg font-semibold">{analysis.metadata.build || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-slate-400 text-sm">File Size</p>
                  <p className="text-lg font-semibold">
                    {(analysis.metadata.file_size / 1024).toFixed(2)} KB
                  </p>
                </div>
                <div>
                  <p className="text-slate-400 text-sm">Copyright</p>
                  <p className="text-lg font-semibold truncate">
                    {analysis.metadata.copyright}
                  </p>
                </div>
              </div>
            </div>

            {/* Risk Assessment */}
            <div className="bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-xl p-6">
              <h2 className="text-2xl font-semibold mb-4">Risk Assessment</h2>

              <div className="flex items-center gap-6 mb-6">
                <div className="flex-1">
                  <div className="flex justify-between mb-2">
                    <span className="text-slate-400">Risk Score</span>
                    <span className={`font-bold ${getRiskColor(analysis.risk_assessment.level)}`}>
                      {analysis.risk_assessment.score}/100
                    </span>
                  </div>
                  <div className="h-4 bg-slate-700 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${
                        analysis.risk_assessment.level === 'LOW'
                          ? 'bg-emerald-500'
                          : analysis.risk_assessment.level === 'MEDIUM'
                          ? 'bg-amber-500'
                          : 'bg-red-500'
                      }`}
                      style={{ width: `${analysis.risk_assessment.score}%` }}
                    />
                  </div>
                </div>
                <div className={`text-4xl font-bold ${getRiskColor(analysis.risk_assessment.level)}`}>
                  {analysis.risk_assessment.level}
                </div>
              </div>

              {analysis.risk_assessment.factors.length > 0 && (
                <div className="space-y-3">
                  <h3 className="font-semibold text-slate-300">Risk Factors:</h3>
                  {analysis.risk_assessment.factors.map((factor, idx) => (
                    <div
                      key={idx}
                      className="bg-slate-800/50 border border-slate-700 rounded-lg p-4"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <p className="font-semibold">{factor.factor}</p>
                          <p className="text-sm text-slate-400 mt-1">{factor.description}</p>
                        </div>
                        <span
                          className={`px-3 py-1 rounded-full text-xs font-semibold ${getSeverityBadge(
                            factor.severity
                          )}`}
                        >
                          {factor.severity.toUpperCase()}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Trading Logic */}
            <div className="bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-xl p-6">
              <h2 className="text-2xl font-semibold mb-4">Trading Logic</h2>

              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                <div className="bg-slate-800/50 rounded-lg p-4">
                  <p className="text-slate-400 text-sm mb-1">Stop Loss</p>
                  <p className={`text-lg font-semibold ${analysis.trading_logic.uses_stop_loss ? 'text-emerald-400' : 'text-red-400'}`}>
                    {analysis.trading_logic.uses_stop_loss ? '✓ Yes' : '✗ No'}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-4">
                  <p className="text-slate-400 text-sm mb-1">Take Profit</p>
                  <p className={`text-lg font-semibold ${analysis.trading_logic.uses_take_profit ? 'text-emerald-400' : 'text-red-400'}`}>
                    {analysis.trading_logic.uses_take_profit ? '✓ Yes' : '✗ No'}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-4">
                  <p className="text-slate-400 text-sm mb-1">Trailing Stop</p>
                  <p className={`text-lg font-semibold ${analysis.trading_logic.uses_trailing_stop ? 'text-emerald-400' : 'text-red-400'}`}>
                    {analysis.trading_logic.uses_trailing_stop ? '✓ Yes' : '✗ No'}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-4">
                  <p className="text-slate-400 text-sm mb-1">Martingale</p>
                  <p className={`text-lg font-semibold ${analysis.trading_logic.uses_martingale ? 'text-red-400' : 'text-emerald-400'}`}>
                    {analysis.trading_logic.uses_martingale ? '⚠ Yes' : '✓ No'}
                  </p>
                </div>
              </div>

              {analysis.trading_logic.indicators.length > 0 && (
                <div className="mt-6">
                  <h3 className="font-semibold text-slate-300 mb-3">Detected Indicators:</h3>
                  <div className="flex flex-wrap gap-2">
                    {analysis.trading_logic.indicators.map((indicator, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1 bg-blue-500/20 text-blue-400 rounded-full text-sm font-medium"
                      >
                        {indicator}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {analysis.trading_logic.timeframes.length > 0 && (
                <div className="mt-4">
                  <h3 className="font-semibold text-slate-300 mb-3">Timeframes:</h3>
                  <div className="flex flex-wrap gap-2">
                    {analysis.trading_logic.timeframes.map((tf, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1 bg-purple-500/20 text-purple-400 rounded-full text-sm font-medium"
                      >
                        {tf}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Recommendations */}
            {analysis.recommendations.length > 0 && (
              <div className="bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-xl p-6">
                <h2 className="text-2xl font-semibold mb-4">💡 Recommendations</h2>
                <div className="space-y-3">
                  {analysis.recommendations.map((rec, idx) => (
                    <div
                      key={idx}
                      className="flex items-start gap-3 bg-blue-500/10 border border-blue-500/30 rounded-lg p-4"
                    >
                      <span className="text-blue-400 font-bold">{idx + 1}.</span>
                      <p className="text-slate-300">{rec}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Parameters */}
            {analysis.parameters.length > 0 && (
              <div className="bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 rounded-xl p-6">
                <h2 className="text-2xl font-semibold mb-4">
                  Detected Parameters ({analysis.parameters.length})
                </h2>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-slate-700">
                        <th className="text-left py-3 px-4 text-slate-400 font-semibold">Name</th>
                        <th className="text-left py-3 px-4 text-slate-400 font-semibold">Type</th>
                        <th className="text-left py-3 px-4 text-slate-400 font-semibold">Default</th>
                        <th className="text-left py-3 px-4 text-slate-400 font-semibold">Optimizable</th>
                      </tr>
                    </thead>
                    <tbody>
                      {analysis.parameters.map((param, idx) => (
                        <tr key={idx} className="border-b border-slate-800 hover:bg-slate-800/50">
                          <td className="py-3 px-4 font-medium">{param.name}</td>
                          <td className="py-3 px-4 text-slate-400">{param.type}</td>
                          <td className="py-3 px-4 font-mono text-sm">{String(param.default_value)}</td>
                          <td className="py-3 px-4">
                            {param.is_optimizable ? (
                              <span className="text-emerald-400">✓</span>
                            ) : (
                              <span className="text-slate-600">-</span>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

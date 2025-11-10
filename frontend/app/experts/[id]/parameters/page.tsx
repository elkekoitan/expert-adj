"use client"

import { useState } from 'react'
import { Save, Copy, Star, TrendingUp, Settings2, ChevronDown, ChevronRight } from 'lucide-react'

// Mock data - will be replaced with API calls
const mockParameters = {
  "GENEL SİSTEM AYARLARI": [
    { name: "MaxCascadeRobots", type: "int", value: 5, default: 5, description: "AKTİF ROBOT SAYISI (1-5)", min: 1, max: 5 },
    { name: "TriggerLevel", type: "int", value: 2, default: 2, description: "TETİKLEME KADEMESİ (1-10)", min: 1, max: 10 },
    { name: "DistancePercent", type: "double", value: 50.0, default: 50.0, description: "MESAFE ÇARPANI (%)" },
    { name: "LotPercent", type: "double", value: 100.0, default: 100.0, description: "LOT ÇARPANI (%)" },
  ],
  "ZAMAN AYARLARI": [
    { name: "StartHour", type: "int", value: 1, default: 1, description: "Başlangıç Saati", min: 0, max: 23 },
    { name: "StartMinute", type: "int", value: 15, default: 15, description: "Başlangıç Dakikası", min: 0, max: 59 },
    { name: "EndHour", type: "int", value: 22, default: 22, description: "Bitiş Saati", min: 0, max: 23 },
    { name: "EndMinute", type: "int", value: 0, default: 0, description: "Bitiş Dakikası", min: 0, max: 59 },
    { name: "LoopWaitMinutes", type: "int", value: 30, default: 30, description: "Döngü Bekleme (Dakika)", min: 1, max: 120 },
  ],
  "TİCARET AYARLARI": [
    { name: "TradeDirection", type: "int", value: 2, default: 2, description: "YÖN: 0=Buy, 1=Sell, 2=İki Yön", min: 0, max: 2 },
    { name: "DailyProfitTarget", type: "double", value: 500.0, default: 500.0, description: "GÜNLÜK KAR HEDEFİ ($)" },
  ],
  "ROBOT 1 - KAR HEDEFLERİ": [
    { name: "Robot1_BuyProfit", type: "double", value: 50.0, default: 50.0, description: "BUY ZİNCİR KAR HEDEFİ ($)" },
    { name: "Robot1_SellProfit", type: "double", value: 50.0, default: 50.0, description: "SELL ZİNCİR KAR HEDEFİ ($)" },
  ],
}

const mockPresets = [
  { id: 1, name: "Conservative - Low Risk", isFavorite: true, tags: ["conservative", "low-risk"] },
  { id: 2, name: "Aggressive - High Return", isFavorite: false, tags: ["aggressive", "high-risk"] },
  { id: 3, name: "Scalping Strategy", isFavorite: true, tags: ["scalping", "short-term"] },
]

export default function ParametersPage() {
  const [parameters, setParameters] = useState(mockParameters)
  const [expandedGroups, setExpandedGroups] = useState<Set<string>>(new Set(Object.keys(mockParameters)))
  const [presetName, setPresetName] = useState("")
  const [showSavePreset, setShowSavePreset] = useState(false)
  const [selectedPreset, setSelectedPreset] = useState<number | null>(null)

  const toggleGroup = (group: string) => {
    const newExpanded = new Set(expandedGroups)
    if (newExpanded.has(group)) {
      newExpanded.delete(group)
    } else {
      newExpanded.add(group)
    }
    setExpandedGroups(newExpanded)
  }

  const handleParameterChange = (group: string, paramIndex: number, value: string) => {
    setParameters(prev => ({
      ...prev,
      [group]: prev[group].map((param, idx) =>
        idx === paramIndex ? { ...param, value: parseFloat(value) || value } : param
      )
    }))
  }

  const handleResetToDefault = (group: string, paramIndex: number) => {
    setParameters(prev => ({
      ...prev,
      [group]: prev[group].map((param, idx) =>
        idx === paramIndex ? { ...param, value: param.default } : param
      )
    }))
  }

  const handleSavePreset = () => {
    // TODO: API call to save preset
    console.log("Saving preset:", presetName, parameters)
    setShowSavePreset(false)
    setPresetName("")
    alert(`Preset "${presetName}" saved successfully!`)
  }

  const handleLoadPreset = (presetId: number) => {
    setSelectedPreset(presetId)
    // TODO: Load preset parameters from API
    alert(`Loading preset #${presetId}`)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            Parameter Editor
          </h1>
          <p className="text-slate-400">SmartMartingale Pro EA v6.0</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar - Presets */}
          <div className="lg:col-span-1">
            <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-6 sticky top-8">
              <div className="flex items-center gap-2 mb-4">
                <Settings2 className="w-5 h-5 text-purple-400" />
                <h2 className="text-xl font-semibold">Presets</h2>
              </div>

              <div className="space-y-2 mb-4">
                {mockPresets.map(preset => (
                  <button
                    key={preset.id}
                    onClick={() => handleLoadPreset(preset.id)}
                    className={`w-full text-left p-3 rounded-lg transition-colors ${
                      selectedPreset === preset.id
                        ? 'bg-blue-600'
                        : 'bg-slate-700/50 hover:bg-slate-700'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-semibold text-sm">{preset.name}</span>
                      {preset.isFavorite && <Star className="w-4 h-4 text-yellow-400 fill-yellow-400" />}
                    </div>
                    <div className="flex flex-wrap gap-1">
                      {preset.tags.map(tag => (
                        <span key={tag} className="text-xs bg-slate-600/50 px-2 py-0.5 rounded-full">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </button>
                ))}
              </div>

              <button
                onClick={() => setShowSavePreset(true)}
                className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 px-4 py-2 rounded-lg font-semibold text-sm transition-colors flex items-center justify-center gap-2"
              >
                <Save className="w-4 h-4" />
                Save as Preset
              </button>
            </div>
          </div>

          {/* Main Content - Parameters */}
          <div className="lg:col-span-3 space-y-6">
            {/* Action Buttons */}
            <div className="flex gap-4">
              <button className="flex-1 bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-xl font-semibold transition-colors flex items-center justify-center gap-2">
                <TrendingUp className="w-5 h-5" />
                Start Optimization
              </button>
              <button className="bg-slate-700 hover:bg-slate-600 px-6 py-3 rounded-xl font-semibold transition-colors flex items-center justify-center gap-2">
                <Copy className="w-5 h-5" />
                Clone
              </button>
            </div>

            {/* Parameter Groups */}
            {Object.entries(parameters).map(([group, params]) => (
              <div
                key={group}
                className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl overflow-hidden"
              >
                {/* Group Header */}
                <button
                  onClick={() => toggleGroup(group)}
                  className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-700/30 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    {expandedGroups.has(group) ? (
                      <ChevronDown className="w-5 h-5 text-blue-400" />
                    ) : (
                      <ChevronRight className="w-5 h-5 text-blue-400" />
                    )}
                    <h3 className="text-lg font-semibold">{group}</h3>
                    <span className="text-sm text-slate-400">({params.length} parameters)</span>
                  </div>
                </button>

                {/* Group Content */}
                {expandedGroups.has(group) && (
                  <div className="px-6 pb-6 space-y-4">
                    {params.map((param, idx) => (
                      <div key={param.name} className="bg-slate-900/50 rounded-xl p-4">
                        <div className="flex items-start justify-between mb-3">
                          <div>
                            <label className="font-mono font-semibold text-sm">{param.name}</label>
                            <p className="text-xs text-slate-400 mt-1">{param.description}</p>
                          </div>
                          <span className="text-xs bg-blue-500/20 text-blue-400 px-2 py-1 rounded">
                            {param.type}
                          </span>
                        </div>

                        <div className="flex gap-3">
                          <input
                            type="number"
                            value={param.value}
                            onChange={(e) => handleParameterChange(group, idx, e.target.value)}
                            step={param.type === 'double' ? '0.01' : '1'}
                            min={param.min}
                            max={param.max}
                            className="flex-1 bg-slate-800 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500"
                          />
                          <button
                            onClick={() => handleResetToDefault(group, idx)}
                            className="bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded-lg text-sm transition-colors"
                            title="Reset to default"
                          >
                            Default: {param.default}
                          </button>
                        </div>

                        {param.min !== undefined && param.max !== undefined && (
                          <div className="mt-2 flex items-center gap-2 text-xs text-slate-400">
                            <span>Range: {param.min} - {param.max}</span>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Save Preset Modal */}
        {showSavePreset && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
            <div className="bg-slate-800 border border-slate-700 rounded-2xl p-8 max-w-md w-full">
              <h3 className="text-2xl font-bold mb-4">Save Preset</h3>
              <input
                type="text"
                value={presetName}
                onChange={(e) => setPresetName(e.target.value)}
                placeholder="Enter preset name..."
                className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-3 mb-6 focus:outline-none focus:border-blue-500"
              />
              <div className="flex gap-4">
                <button
                  onClick={() => setShowSavePreset(false)}
                  className="flex-1 bg-slate-700 hover:bg-slate-600 px-6 py-3 rounded-lg font-semibold transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleSavePreset}
                  disabled={!presetName}
                  className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-slate-600 disabled:to-slate-700 px-6 py-3 rounded-lg font-semibold transition-colors disabled:cursor-not-allowed"
                >
                  Save
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export type RiskLevel = 'low' | 'medium' | 'high' | 'extreme'

export interface RiskAnalysis {
  risk_score: number
  risk_level: RiskLevel
  factors: RiskFactor[]
  prediction: {
    next_drawdown: number
    confidence: number
  }
}

export interface RiskFactor {
  name: string
  value: number
  impact: 'low' | 'medium' | 'high'
  description: string
}

export interface Recommendation {
  ea_id: string
  ea_name: string
  confidence: number
  reason: string
  suggested_params?: Record<string, any>
  expected_performance?: {
    profit_factor: number
    sharpe_ratio: number
    max_drawdown: number
  }
}

export interface EquityPrediction {
  historical: number[]
  predicted: number[]
  confidence_intervals: {
    lower_95: number[]
    lower_75: number[]
    median: number[]
    upper_75: number[]
    upper_95: number[]
  }
  dates: string[]
}

export interface MonteCarloResult {
  scenarios: number[][]
  statistics: {
    mean_final: number
    median_final: number
    std_final: number
    percentile_5: number
    percentile_25: number
    percentile_75: number
    percentile_95: number
    risk_of_ruin: number
  }
}

export interface CorrelationMatrix {
  ea_ids: string[]
  ea_names: string[]
  matrix: number[][]
  diversification_score: number
}

export interface AdvancedMetrics {
  calmar_ratio: number
  sortino_ratio: number
  ulcer_index: number
  k_ratio: number
  gain_to_pain_ratio: number
  max_drawdown_duration: number
  recovery_factor: number
  profit_to_drawdown_ratio: number
}

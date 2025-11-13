export type BacktestStatus = 'queued' | 'running' | 'completed' | 'failed'
export type OptimizationMethod = 'genetic' | 'grid' | 'bayesian' | 'random'
export type TargetMetric =
  | 'profit_factor'
  | 'sharpe_ratio'
  | 'net_profit'
  | 'max_drawdown'
  | 'win_rate'

export interface BacktestResult {
  id: string
  optimization_session_id?: string
  ea_version_id: string
  symbol: string
  timeframe: string
  test_from: string
  test_to: string
  parameters: Record<string, any>
  is_training: boolean
  is_oos: boolean
  initial_deposit: number
  leverage: number
  modeling_quality: number
  net_profit: number
  gross_profit: number
  gross_loss: number
  profit_factor: number
  expected_payoff: number
  max_drawdown: number
  max_drawdown_percent: number
  relative_drawdown: number
  total_trades: number
  winning_trades: number
  losing_trades: number
  win_rate: number
  largest_profit_trade: number
  largest_loss_trade: number
  average_profit_trade: number
  average_loss_trade: number
  max_consecutive_wins: number
  max_consecutive_losses: number
  sharpe_ratio?: number
  sortino_ratio?: number
  calmar_ratio?: number
  recovery_factor?: number
  report_html_path?: string
  report_xml_path?: string
  trades_csv_path?: string
  created_at: string
}

export interface OptimizationSession {
  id: string
  ea_version_id: string
  owner_id: string
  name: string
  symbols: string[]
  timeframes: string[]
  date_from: string
  date_to: string
  optimization_method: OptimizationMethod
  target_metric: TargetMetric
  walk_forward_enabled: boolean
  wf_config?: Record<string, any>
  status: BacktestStatus
  total_iterations: number
  completed_iterations: number
  best_parameters?: Record<string, any>
  best_score?: number
  started_at?: string
  completed_at?: string
  error_message?: string
  created_at: string
}

export interface BacktestRun {
  id: string
  preset_id: string
  ea_version_id: string
  symbol: string
  timeframe: string
  date_from: string
  date_to: string
  engine: 'mt4' | 'mt5'
  parameters: Record<string, any>
  status: BacktestStatus
  metrics?: Record<string, any>
  report_ref?: string
  error_message?: string
  started_at?: string
  completed_at?: string
  created_at: string
}

export interface CreateBacktestRequest {
  symbol?: string
  timeframe?: string
  date_from?: string
  date_to?: string
}

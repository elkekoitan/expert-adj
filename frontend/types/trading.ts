export type AccountType = 'demo' | 'live'
export type TradeType = 'BUY' | 'SELL'
export type OrderType = 'BUY' | 'SELL' | 'BUY_LIMIT' | 'SELL_LIMIT' | 'BUY_STOP' | 'SELL_STOP'
export type SessionStatus = 'pending' | 'running' | 'paused' | 'stopped' | 'error'

export interface TradingAccount {
  id: string
  owner_id: string
  platform: 'MT4' | 'MT5'
  broker_server: string
  account_number: string
  account_type: AccountType
  label?: string
  is_active: boolean
  is_connected: boolean
  balance: number
  equity: number
  margin: number
  free_margin: number
  leverage: number
  currency: string
  last_heartbeat?: string
  meta_data?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface LiveSession {
  id: string
  account_id: string
  ea_version_id: string
  symbol: string
  timeframe: string
  parameters: Record<string, any>
  status: SessionStatus
  initial_balance: number
  current_profit: number
  peak_profit: number
  current_drawdown: number
  max_drawdown: number
  total_trades: number
  winning_trades: number
  losing_trades: number
  threshold_policy?: Record<string, any>
  started_at?: string
  stopped_at?: string
  last_heartbeat_at?: string
  created_at: string
  updated_at: string
}

export interface Position {
  id: string
  session_id: string
  ticket: string
  symbol: string
  position_type: TradeType
  volume: number
  open_price: number
  current_price: number
  stop_loss?: number
  take_profit?: number
  profit: number
  commission: number
  swap: number
  open_time: string
}

export interface Trade {
  id: string
  session_id: string
  ticket: string
  symbol: string
  trade_type: TradeType
  volume: number
  open_price: number
  close_price: number
  stop_loss?: number
  take_profit?: number
  profit: number
  commission: number
  swap: number
  open_time: string
  close_time: string
  comment?: string
}

export interface AccountInfo {
  balance: number
  equity: number
  margin: number
  free_margin: number
  profit: number
  currency: string
}

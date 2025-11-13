import { create } from 'zustand'

interface Position {
  ticket: string
  symbol: string
  type: 'BUY' | 'SELL'
  volume: number
  open_price: number
  current_price: number
  stop_loss?: number
  take_profit?: number
  profit: number
  open_time: string
}

interface AccountInfo {
  balance: number
  equity: number
  margin: number
  free_margin: number
  profit: number
  currency: string
}

interface TradingState {
  accountInfo: AccountInfo | null
  positions: Position[]
  isConnected: boolean
  isLoading: boolean
  error: string | null
  
  setAccountInfo: (info: AccountInfo) => void
  setPositions: (positions: Position[]) => void
  addPosition: (position: Position) => void
  updatePosition: (ticket: string, updates: Partial<Position>) => void
  removePosition: (ticket: string) => void
  setConnected: (connected: boolean) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  reset: () => void
}

export const useTradingStore = create<TradingState>((set) => ({
  accountInfo: null,
  positions: [],
  isConnected: false,
  isLoading: false,
  error: null,

  setAccountInfo: (info) => set({ accountInfo: info }),
  
  setPositions: (positions) => set({ positions }),
  
  addPosition: (position) =>
    set((state) => ({ positions: [...state.positions, position] })),
  
  updatePosition: (ticket, updates) =>
    set((state) => ({
      positions: state.positions.map((pos) =>
        pos.ticket === ticket ? { ...pos, ...updates } : pos
      ),
    })),
  
  removePosition: (ticket) =>
    set((state) => ({
      positions: state.positions.filter((pos) => pos.ticket !== ticket),
    })),
  
  setConnected: (connected) => set({ isConnected: connected }),
  
  setLoading: (loading) => set({ isLoading: loading }),
  
  setError: (error) => set({ error }),
  
  reset: () =>
    set({
      accountInfo: null,
      positions: [],
      isConnected: false,
      error: null,
    }),
}))

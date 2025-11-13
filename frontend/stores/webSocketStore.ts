import { create } from 'zustand'

interface WebSocketState {
  connected: boolean
  connecting: boolean
  error: string | null

  setConnected: (connected: boolean) => void
  setConnecting: (connecting: boolean) => void
  setError: (error: string | null) => void
}

export const useWebSocketStore = create<WebSocketState>((set) => ({
  connected: false,
  connecting: false,
  error: null,

  setConnected: (connected) => set({ connected }),
  setConnecting: (connecting) => set({ connecting }),
  setError: (error) => set({ error }),
}))

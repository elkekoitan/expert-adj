import { create } from 'zustand'

interface EA {
  id: string
  name: string
  description?: string
  platform: 'MT4' | 'MT5'
  tags?: string[]
  is_active: boolean
  created_at: string
}

interface EAState {
  eas: EA[]
  selectedEA: EA | null
  isLoading: boolean
  error: string | null
  
  setEAs: (eas: EA[]) => void
  setSelectedEA: (ea: EA | null) => void
  addEA: (ea: EA) => void
  updateEA: (id: string, updates: Partial<EA>) => void
  removeEA: (id: string) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
}

export const useEAStore = create<EAState>((set) => ({
  eas: [],
  selectedEA: null,
  isLoading: false,
  error: null,

  setEAs: (eas) => set({ eas }),
  
  setSelectedEA: (ea) => set({ selectedEA: ea }),
  
  addEA: (ea) => set((state) => ({ eas: [...state.eas, ea] })),
  
  updateEA: (id, updates) =>
    set((state) => ({
      eas: state.eas.map((ea) => (ea.id === id ? { ...ea, ...updates } : ea)),
    })),
  
  removeEA: (id) =>
    set((state) => ({
      eas: state.eas.filter((ea) => ea.id !== id),
    })),
  
  setLoading: (loading) => set({ isLoading: loading }),
  
  setError: (error) => set({ error }),
}))

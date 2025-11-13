import { useQuery, useMutation, useQueryClient, UseQueryOptions } from '@tanstack/react-query'
import { api } from '@/lib/api'

export function useBacktests(options?: UseQueryOptions<any[]>) {
  return useQuery({
    queryKey: ['backtests'],
    queryFn: () => api.backtests.list(),
    ...options,
  })
}

export function useBacktest(id: string, options?: UseQueryOptions<any>) {
  return useQuery({
    queryKey: ['backtest', id],
    queryFn: () => api.backtests.get(id),
    enabled: !!id,
    ...options,
  })
}

export function useCreateBacktest() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: any) => api.backtests.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['backtests'] })
    },
  })
}

export function useUpdateBacktest() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: any }) => api.backtests.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['backtests'] })
      queryClient.invalidateQueries({ queryKey: ['backtest', variables.id] })
    },
  })
}

export function useEAs(options?: UseQueryOptions<any[]>) {
  return useQuery({
    queryKey: ['eas'],
    queryFn: () => api.eas.list(),
    ...options,
  })
}

export function useEA(id: string, options?: UseQueryOptions<any>) {
  return useQuery({
    queryKey: ['ea', id],
    queryFn: () => api.eas.get(id),
    enabled: !!id,
    ...options,
  })
}

export function useUploadEA() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (file: File) => api.eas.upload(file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['eas'] })
    },
  })
}

export function useDeleteEA() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => api.eas.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['eas'] })
    },
  })
}

export function usePresets(eaId?: string, options?: UseQueryOptions<any[]>) {
  return useQuery({
    queryKey: eaId ? ['presets', eaId] : ['presets'],
    queryFn: () => api.presets.list(eaId),
    ...options,
  })
}

export function useCreatePreset() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: any) => api.presets.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['presets'] })
    },
  })
}

export function useStrategyPresets(options?: UseQueryOptions<any[]>) {
  return useQuery({
    queryKey: ['strategy-presets'],
    queryFn: () => api.strategyPresets.list(),
    ...options,
  })
}

export function useCreateBacktestForPreset() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ presetId, data }: { presetId: string; data: any }) =>
      api.strategyPresets.createBacktest(presetId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['backtests'] })
    },
  })
}

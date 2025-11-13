import { useEffect, useState } from 'react'
import { wsClient } from '@/lib/websocket'
import { Socket } from 'socket.io-client'
import { useAuthStore } from '@/stores/authStore'

export function useWebSocket() {
  const [socket, setSocket] = useState<Socket | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const { token } = useAuthStore()

  useEffect(() => {
    if (!token) return

    const ws = wsClient.connect(token)
    setSocket(ws)

    const handleConnect = () => setIsConnected(true)
    const handleDisconnect = () => setIsConnected(false)

    ws.on('connect', handleConnect)
    ws.on('disconnect', handleDisconnect)

    return () => {
      ws.off('connect', handleConnect)
      ws.off('disconnect', handleDisconnect)
      wsClient.disconnect()
    }
  }, [token])

  const emit = (event: string, data?: any) => {
    if (socket?.connected) {
      socket.emit(event, data)
    }
  }

  const on = (event: string, callback: (...args: any[]) => void) => {
    if (socket) {
      socket.on(event, callback)
    }
  }

  const off = (event: string, callback?: (...args: any[]) => void) => {
    if (socket) {
      socket.off(event, callback)
    }
  }

  return {
    socket,
    isConnected,
    emit,
    on,
    off,
  }
}

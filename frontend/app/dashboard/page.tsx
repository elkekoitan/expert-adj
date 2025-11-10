'use client'

import { useEffect, useState } from 'react'
import { io, Socket } from 'socket.io-client'

interface Position {
  ticket: number
  symbol: string
  type: string
  volume: number
  price_open: number
  price_current: number
  profit: number
  open_time: string
}

interface AccountInfo {
  balance: number
  equity: number
  margin: number
  free_margin: number
  profit: number
}

export default function DashboardPage() {
  const [socket, setSocket] = useState<Socket | null>(null)
  const [connected, setConnected] = useState(false)
  const [accountInfo, setAccountInfo] = useState<AccountInfo>({
    balance: 0,
    equity: 0,
    margin: 0,
    free_margin: 0,
    profit: 0
  })
  const [positions, setPositions] = useState<Position[]>([])
  const [recentTrades, setRecentTrades] = useState<any[]>([])

  useEffect(() => {
    // Connect to WebSocket
    const newSocket = io('http://localhost:8000')

    newSocket.on('connect', () => {
      console.log('WebSocket connected')
      setConnected(true)

      // Join user room
      newSocket.emit('join_user_room', { user_id: 'demo_user' })
    })

    newSocket.on('disconnect', () => {
      console.log('WebSocket disconnected')
      setConnected(false)
    })

    // Listen for account updates
    newSocket.on('account_update', (data: any) => {
      console.log('Account update:', data)
      setAccountInfo(data.data)
    })

    // Listen for position updates
    newSocket.on('positions_update', (data: any) => {
      console.log('Positions update:', data)
      setPositions(data.positions)
    })

    // Listen for trade events
    newSocket.on('trade_opened', (data: any) => {
      console.log('Trade opened:', data)
      setRecentTrades(prev => [data.trade, ...prev].slice(0, 10))
    })

    newSocket.on('trade_closed', (data: any) => {
      console.log('Trade closed:', data)
      setRecentTrades(prev => [data.trade, ...prev].slice(0, 10))
    })

    setSocket(newSocket)

    return () => {
      newSocket.close()
    }
  }, [])

  const totalProfit = positions.reduce((sum, pos) => sum + pos.profit, 0)
  const totalPositions = positions.length

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🚀 MT Expert Optimizer - Live Dashboard
          </h1>
          <div className="flex items-center gap-2">
            <div className={`h-3 w-3 rounded-full ${connected ? 'bg-green-500' : 'bg-red-500'}`} />
            <span className="text-sm text-gray-600">
              {connected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
        </div>

        {/* Account Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm text-gray-600 mb-1">Balance</div>
            <div className="text-2xl font-bold text-gray-900">
              ${accountInfo.balance.toFixed(2)}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm text-gray-600 mb-1">Equity</div>
            <div className="text-2xl font-bold text-gray-900">
              ${accountInfo.equity.toFixed(2)}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm text-gray-600 mb-1">Profit</div>
            <div className={`text-2xl font-bold ${accountInfo.profit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              ${accountInfo.profit.toFixed(2)}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm text-gray-600 mb-1">Free Margin</div>
            <div className="text-2xl font-bold text-gray-900">
              ${accountInfo.free_margin.toFixed(2)}
            </div>
          </div>
        </div>

        {/* Live Positions */}
        <div className="bg-white rounded-lg shadow mb-8">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">
              📊 Open Positions ({totalPositions})
            </h2>
            <div className="text-sm text-gray-600">
              Total P&L: <span className={totalProfit >= 0 ? 'text-green-600' : 'text-red-600'}>
                ${totalProfit.toFixed(2)}
              </span>
            </div>
          </div>
          <div className="overflow-x-auto">
            {positions.length > 0 ? (
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Ticket
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Symbol
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Type
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Volume
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Open Price
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Current Price
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Profit
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {positions.map((pos) => (
                    <tr key={pos.ticket} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        #{pos.ticket}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {pos.symbol}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          pos.type === 'BUY' ? 'bg-blue-100 text-blue-800' : 'bg-red-100 text-red-800'
                        }`}>
                          {pos.type}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {pos.volume.toFixed(2)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {pos.price_open.toFixed(5)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {pos.price_current.toFixed(5)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <span className={pos.profit >= 0 ? 'text-green-600 font-semibold' : 'text-red-600 font-semibold'}>
                          ${pos.profit.toFixed(2)}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <div className="px-6 py-12 text-center text-gray-500">
                No open positions
              </div>
            )}
          </div>
        </div>

        {/* Recent Trades */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">
              📈 Recent Trades
            </h2>
          </div>
          <div className="p-6">
            {recentTrades.length > 0 ? (
              <div className="space-y-4">
                {recentTrades.map((trade, index) => (
                  <div key={index} className="border-l-4 border-blue-500 pl-4">
                    <div className="text-sm text-gray-600">
                      {new Date(trade.time || Date.now()).toLocaleString()}
                    </div>
                    <div className="font-medium">
                      {trade.symbol} {trade.type} {trade.volume} lots
                    </div>
                    <div className="text-sm text-gray-600">
                      Profit: <span className={trade.profit >= 0 ? 'text-green-600' : 'text-red-600'}>
                        ${trade.profit?.toFixed(2) || '0.00'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center text-gray-500 py-8">
                No recent trades
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

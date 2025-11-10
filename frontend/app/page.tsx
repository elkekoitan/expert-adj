export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold text-center mb-8">
          🚀 MT Expert Optimizer
        </h1>
        <p className="text-center text-xl text-gray-600 mb-12">
          Automated MT4/MT5 Expert Advisor Optimization Platform
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="border rounded-lg p-6 hover:shadow-lg transition">
            <h2 className="text-xl font-semibold mb-2">📚 EA Library</h2>
            <p className="text-gray-600">Upload and manage your Expert Advisors</p>
          </div>

          <div className="border rounded-lg p-6 hover:shadow-lg transition">
            <h2 className="text-xl font-semibold mb-2">⚡ Optimization</h2>
            <p className="text-gray-600">Automatic parameter optimization</p>
          </div>

          <div className="border rounded-lg p-6 hover:shadow-lg transition">
            <h2 className="text-xl font-semibold mb-2">📊 Analytics</h2>
            <p className="text-gray-600">Real-time performance monitoring</p>
          </div>
        </div>

        <div className="mt-12 text-center text-sm text-gray-500">
          <p>API Status: <span className="text-green-600">● Connected</span></p>
        </div>
      </div>
    </main>
  )
}

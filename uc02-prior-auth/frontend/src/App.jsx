import { useState } from 'react'

function App() {
  const [healthStatus, setHealthStatus] = useState('Checking backend...')

  const checkBackendHealth = async () => {
    try {
      const res = await fetch('http://localhost:8000/health')
      const data = await res.json()
      setHealthStatus(`Connected! Backend status: ${data.status} (env: ${data.environment})`)
    } catch (err) {
      setHealthStatus('Error: Backend is unreachable. Make sure it is running on port 8000.')
    }
  }

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col justify-between font-sans">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-indigo-500 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/30">
              PA
            </div>
            <span className="font-bold text-lg tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
              PriorAuth Companion
            </span>
          </div>
          <div className="flex items-center gap-4">
            <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              Phase 0 - Foundation
            </span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-4xl mx-auto w-full px-4 py-16 flex flex-col justify-center">
        <div className="text-center space-y-6">
          <h1 className="text-5xl font-extrabold tracking-tight text-white sm:text-6xl bg-gradient-to-b from-white to-slate-400 bg-clip-text text-transparent leading-none">
            UC02 Prior Authorization
          </h1>
          <p className="max-w-2xl mx-auto text-lg text-slate-400">
            A human-in-the-loop Prior Authorization decision-support system to streamline clinical triage and policy reviews.
          </p>

          <div className="pt-8 max-w-md mx-auto">
            <div className="p-6 rounded-2xl bg-slate-800/50 border border-slate-700/50 backdrop-blur-sm shadow-xl space-y-4">
              <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">
                Backend Connection Test
              </h2>
              <p className="text-sm text-slate-400 break-words font-mono bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                {healthStatus}
              </p>
              <button
                onClick={checkBackendHealth}
                className="w-full py-2 px-4 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white font-medium rounded-lg shadow-lg shadow-indigo-600/20 transition-all duration-150 flex items-center justify-center gap-2 cursor-pointer"
              >
                Test API Connection
              </button>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 py-8 bg-slate-950/40">
        <div className="max-w-7xl mx-auto px-4 text-center text-xs text-slate-500">
          UC02 — Prior Authorization Triage & Policy Companion. All rights reserved.
        </div>
      </footer>
    </div>
  )
}

export default App

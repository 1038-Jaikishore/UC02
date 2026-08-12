import { useState, useEffect } from 'react'
import Dashboard from './pages/Dashboard'
import NewAuthorization from './pages/NewAuthorization'
import AuthorizationDetails from './pages/AuthorizationDetails'
import ReviewResult from './pages/ReviewResult'
import {
  fetchAuthorizations,
  createAuthorization,
  updateAuthorizationStatus,
  checkHealth
} from './services/api'

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [authorizations, setAuthorizations] = useState([])
  const [selectedAuthId, setSelectedAuthId] = useState(null)
  const [healthStatus, setHealthStatus] = useState('Checking backend...')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const loadAuthorizations = async () => {
    setLoading(true)
    setError('')
    try {
      const data = await fetchAuthorizations()
      setAuthorizations(data)
      setHealthStatus('Connected to backend')
    } catch (err) {
      setError('Connection Alert: The backend server is unreachable. Check your network or make sure the API is running on port 8000.')
      setHealthStatus('Backend Offline')
      setAuthorizations([]) // Clear or keep empty
    } finally {
      setLoading(false)
    }
  }

  // Load list on startup
  useEffect(() => {
    loadAuthorizations()
  }, [])

  const checkBackendHealth = async () => {
    setHealthStatus('Checking...')
    try {
      const data = await checkHealth()
      setHealthStatus(`Connected! Backend status: ${data.status} (env: ${data.environment})`)
      setError('')
      // Reload authorizations if it succeeded
      const listData = await fetchAuthorizations()
      setAuthorizations(listData)
    } catch (err) {
      setHealthStatus('Backend Offline')
      setError('Connection Alert: The backend server is unreachable. Make sure the API is running on port 8000.')
    }
  }

  // Get active authorization details
  const activeAuth = authorizations.find(a => a.id === selectedAuthId)

  // Navigate helper
  const handleNavigate = (page) => {
    setCurrentPage(page)
  }

  // Add new authorization request handler
  const handleAddAuthorization = async (newAuthData) => {
    try {
      const createdAuth = await createAuthorization(newAuthData)
      setAuthorizations(prev => [createdAuth, ...prev])
      setSelectedAuthId(createdAuth.id)
      setCurrentPage('details') // Redirect straight to details page as per Phase 4 flow
    } catch (err) {
      // rethrow to be caught in form component
      throw err
    }
  }

  // Update request status helper
  const handleUpdateStatus = async (id, newStatus) => {
    try {
      const updatedAuth = await updateAuthorizationStatus(id, newStatus)
      setAuthorizations(prev =>
        prev.map(auth => (auth.id === id ? updatedAuth : auth))
      )
    } catch (err) {
      console.error('Failed to update status:', err)
      alert('Failed to save reviewer decision: backend is offline.')
    }
  }

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col justify-between font-sans">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <button 
            onClick={() => handleNavigate('dashboard')} 
            className="flex items-center gap-3 cursor-pointer group bg-transparent border-0"
          >
            <div className="w-8 h-8 rounded-lg bg-indigo-500 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/30 group-hover:scale-105 transition-all">
              PA
            </div>
            <span className="font-bold text-lg tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent group-hover:text-white transition-all">
              PriorAuth Companion
            </span>
          </button>
          <div className="flex items-center gap-4">
            <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-pulse"></span>
              Phase 4 - Integrated
            </span>
          </div>
        </div>
      </header>

      {/* Connection Warning Banner */}
      {error && (
        <div className="bg-rose-500/10 border-b border-rose-500/20 text-rose-400 py-3 px-4 text-xs font-semibold text-center flex items-center justify-center gap-2">
          <svg className="w-4 h-4 animate-pulse flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <span>{error}</span>
          <button 
            onClick={loadAuthorizations} 
            className="ml-3 px-2 py-0.5 bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 rounded font-bold cursor-pointer transition"
          >
            Retry
          </button>
        </div>
      )}

      {/* Main Content */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="flex flex-col items-center justify-center py-12 space-y-3">
            <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
            <span className="text-sm text-slate-400">Loading requests...</span>
          </div>
        ) : (
          <>
            {currentPage === 'dashboard' && (
              <Dashboard
                authorizations={authorizations}
                onNavigate={handleNavigate}
                setSelectedAuthId={setSelectedAuthId}
              />
            )}
            {currentPage === 'new-auth' && (
              <NewAuthorization
                onNavigate={handleNavigate}
                onAddAuthorization={handleAddAuthorization}
              />
            )}
            {currentPage === 'details' && (
              <AuthorizationDetails
                auth={activeAuth}
                onNavigate={handleNavigate}
              />
            )}
            {currentPage === 'review' && (
              <ReviewResult
                auth={activeAuth}
                onNavigate={handleNavigate}
                onUpdateStatus={handleUpdateStatus}
              />
            )}
          </>
        )}
      </main>

      {/* Footer / Connection bar */}
      <footer className="border-t border-slate-800/80 bg-slate-950/40">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex flex-col sm:flex-row justify-between items-center gap-4">
          <div className="text-xs text-slate-500">
            UC02 — Prior Authorization Triage & Policy Companion. Phase 4 Persistent UI.
          </div>
          <div className="flex items-center gap-3">
            <span className="text-xs text-slate-400 font-mono">{healthStatus}</span>
            <button
              onClick={checkBackendHealth}
              className="py-1 px-2.5 bg-slate-800 hover:bg-slate-700 active:bg-slate-750 text-[10px] font-medium text-slate-300 rounded border border-slate-700/60 cursor-pointer"
            >
              Verify Connection
            </button>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App

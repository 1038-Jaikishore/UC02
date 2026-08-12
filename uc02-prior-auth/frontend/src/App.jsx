import { useState } from 'react'
import Dashboard from './pages/Dashboard'
import NewAuthorization from './pages/NewAuthorization'
import AuthorizationDetails from './pages/AuthorizationDetails'
import ReviewResult from './pages/ReviewResult'

const INITIAL_AUTHORIZATIONS = [
  {
    id: 'PA-4011',
    patient_id: 'PT-5510',
    diagnosis: 'Severe primary osteoarthritis of right knee',
    diagnosis_code: 'M17.11',
    requested_procedure: 'Total knee arthroplasty, right',
    cpt_code: '27447',
    clinical_notes: 'Patient is a 68-year-old female with severe right knee pain for >12 months. Unable to walk >1 block. Conservative treatments failed including physical therapy (12 weeks) and NSAIDs. X-rays reveal bone-on-bone joint space narrowing.',
    priority: 'Standard',
    status: 'PENDING_REVIEW',
    created_at: '2026-08-10',
    supporting_documents: ['xray_right_knee.pdf', 'clinical_summary_PT-5510.pdf']
  },
  {
    id: 'PA-4012',
    patient_id: 'PT-7721',
    diagnosis: 'Spinal stenosis, lumbar region',
    diagnosis_code: 'M48.061',
    requested_procedure: 'Decompression laminectomy, lumbar, single segment',
    cpt_code: '63047',
    clinical_notes: 'Patient reports progressive bilateral leg pain and numbness aggravated by walking. MRI reveals severe central canal stenosis at L4-L5. Symptoms unresponsive to epidural steroid injections.',
    priority: 'Urgent',
    status: 'PENDING_REVIEW',
    created_at: '2026-08-11',
    supporting_documents: ['mri_lumbar_spine.pdf']
  },
  {
    id: 'PA-4013',
    patient_id: 'PT-2294',
    diagnosis: 'Degenerative meniscus tear, medial',
    diagnosis_code: 'S83.242A',
    requested_procedure: 'Arthroscopic partial meniscectomy, medial',
    cpt_code: '29881',
    clinical_notes: 'Patient reports persistent mechanical catching and locking in the medial knee compartment for 6 months. Failed conservative management.',
    priority: 'Standard',
    status: 'APPROVED',
    created_at: '2026-08-08',
    supporting_documents: ['mri_medial_meniscus.pdf']
  }
]

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [authorizations, setAuthorizations] = useState(INITIAL_AUTHORIZATIONS)
  const [selectedAuthId, setSelectedAuthId] = useState(null)
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

  // Get active authorization details
  const activeAuth = authorizations.find(a => a.id === selectedAuthId)

  // Navigate helper
  const handleNavigate = (page) => {
    setCurrentPage(page)
  }

  // Add new authorization request handler
  const handleAddAuthorization = (newAuthData) => {
    const newId = `PA-${Math.floor(1000 + Math.random() * 9000)}`
    const today = new Date().toISOString().split('T')[0]
    
    const newAuth = {
      ...newAuthData,
      id: newId,
      status: 'PENDING_REVIEW',
      created_at: today,
      supporting_documents: ['uploaded_clinical_summary.pdf'] // Mock files attached
    }

    setAuthorizations([newAuth, ...authorizations])
    setCurrentPage('dashboard')
  }

  // Update request status helper
  const handleUpdateStatus = (id, newStatus) => {
    setAuthorizations(prev =>
      prev.map(auth => (auth.id === id ? { ...auth, status: newStatus } : auth))
    )
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
              Phase 1 - Reviewer UI
            </span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
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
      </main>

      {/* Footer / Connection bar */}
      <footer className="border-t border-slate-800/80 bg-slate-950/40">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex flex-col sm:flex-row justify-between items-center gap-4">
          <div className="text-xs text-slate-500">
            UC02 — Prior Authorization Triage & Policy Companion. Phase 1 Dummy Reviewer UI.
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

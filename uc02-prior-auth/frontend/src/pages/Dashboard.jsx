import React, { useState } from 'react'

export default function Dashboard({ authorizations, onNavigate, setSelectedAuthId }) {
  const [searchTerm, setSearchTerm] = useState('')

  // Metrics calculation
  const total = authorizations.length
  const pending = authorizations.filter(a => a.status === 'PENDING_REVIEW').length
  const approved = authorizations.filter(a => a.status === 'APPROVED').length
  const urgent = authorizations.filter(a => a.priority === 'Urgent').length

  // Filtering list
  const filteredAuths = authorizations.filter(a => 
    a.patient_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
    a.diagnosis.toLowerCase().includes(searchTerm.toLowerCase()) ||
    a.id.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleViewDetails = (id) => {
    setSelectedAuthId(id)
    onNavigate('details')
  }

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Reviewer Dashboard</h1>
          <p className="text-sm text-slate-400">Manage and audit prior authorization triage requests.</p>
        </div>
        <button
          onClick={() => onNavigate('new-auth')}
          className="py-2.5 px-4 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white font-medium rounded-lg shadow-lg shadow-indigo-600/20 transition-all duration-150 flex items-center gap-2 cursor-pointer text-sm"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          New Authorization
        </button>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-6 bg-slate-800/40 border border-slate-700/50 rounded-xl backdrop-blur-sm shadow-md">
          <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Requests</div>
          <div className="mt-2 text-3xl font-extrabold text-white">{total}</div>
        </div>
        <div className="p-6 bg-slate-800/40 border border-slate-700/50 rounded-xl backdrop-blur-sm shadow-md">
          <div className="text-xs font-semibold text-amber-400 uppercase tracking-wider">Pending Review</div>
          <div className="mt-2 text-3xl font-extrabold text-white">{pending}</div>
        </div>
        <div className="p-6 bg-slate-800/40 border border-slate-700/50 rounded-xl backdrop-blur-sm shadow-md">
          <div className="text-xs font-semibold text-emerald-400 uppercase tracking-wider">Approved</div>
          <div className="mt-2 text-3xl font-extrabold text-white">{approved}</div>
        </div>
        <div className="p-6 bg-slate-800/40 border border-slate-700/50 rounded-xl backdrop-blur-sm shadow-md">
          <div className="text-xs font-semibold text-rose-400 uppercase tracking-wider">Urgent Priority</div>
          <div className="mt-2 text-3xl font-extrabold text-white">{urgent}</div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="flex items-center bg-slate-800/30 border border-slate-700/50 rounded-xl px-4 py-3 shadow-inner">
        <svg className="w-5 h-5 text-slate-400 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          type="text"
          placeholder="Search by Authorization ID, Patient ID, or Diagnosis..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="bg-transparent border-0 outline-none w-full text-slate-200 placeholder-slate-500 text-sm focus:ring-0"
        />
      </div>

      {/* Table / List */}
      <div className="bg-slate-850 border border-slate-750 rounded-xl overflow-hidden shadow-lg">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-700/50 bg-slate-800/30 text-xs font-semibold text-slate-350 uppercase tracking-wider">
                <th className="py-4 px-6">Auth ID</th>
                <th className="py-4 px-6">Patient ID</th>
                <th className="py-4 px-6">Diagnosis</th>
                <th className="py-4 px-6">Procedure</th>
                <th className="py-4 px-6">Priority</th>
                <th className="py-4 px-6">Status</th>
                <th className="py-4 px-6 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-sm text-slate-300">
              {filteredAuths.length > 0 ? (
                filteredAuths.map((auth) => (
                  <tr key={auth.id} className="hover:bg-slate-800/20 transition-all duration-150">
                    <td className="py-4 px-6 font-mono text-xs text-indigo-400 font-semibold">{auth.id}</td>
                    <td className="py-4 px-6 font-mono text-xs">{auth.patient_id}</td>
                    <td className="py-4 px-6 truncate max-w-[180px]" title={auth.diagnosis}>
                      {auth.diagnosis}
                      <span className="block text-xs text-slate-500 font-mono mt-0.5">{auth.diagnosis_code}</span>
                    </td>
                    <td className="py-4 px-6 truncate max-w-[180px]" title={auth.requested_procedure}>
                      {auth.requested_procedure}
                      <span className="block text-xs text-slate-500 font-mono mt-0.5">CPT: {auth.cpt_code}</span>
                    </td>
                    <td className="py-4 px-6">
                      <span className={`inline-flex px-2 py-0.5 rounded-full text-xs font-medium ${
                        auth.priority === 'Urgent'
                          ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                          : 'bg-slate-700/40 text-slate-400 border border-slate-650'
                      }`}>
                        {auth.priority}
                      </span>
                    </td>
                    <td className="py-4 px-6">
                      <span className={`inline-flex px-2 py-0.5 rounded-full text-xs font-medium ${
                        auth.status === 'APPROVED'
                          ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                          : auth.status === 'DENIED'
                          ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                          : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                      }`}>
                        {auth.status.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="py-4 px-6 text-right">
                      <button
                        onClick={() => handleViewDetails(auth.id)}
                        className="py-1 px-3 text-xs bg-slate-700/60 hover:bg-slate-700 hover:text-white border border-slate-600/50 hover:border-slate-500/50 rounded-md transition-all duration-150 cursor-pointer font-medium"
                      >
                        View
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="7" className="text-center py-8 text-slate-500">
                    No authorization requests found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

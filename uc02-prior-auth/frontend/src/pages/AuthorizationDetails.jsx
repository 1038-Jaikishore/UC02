import React from 'react'

export default function AuthorizationDetails({ auth, onNavigate }) {
  if (!auth) {
    return (
      <div className="text-center py-12 text-slate-400">
        Authorization request not found. Go back to the{' '}
        <button onClick={() => onNavigate('dashboard')} className="text-indigo-400 underline">
          Dashboard
        </button>
        .
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-slate-800 pb-4">
        <div className="flex items-center gap-3">
          <button
            onClick={() => onNavigate('dashboard')}
            className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg cursor-pointer transition-all duration-150 border border-slate-700/50"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </button>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-mono text-lg font-bold text-indigo-400">{auth.id}</span>
              <span className={`inline-flex px-2 py-0.5 rounded-full text-[10px] font-medium ${
                auth.priority === 'Urgent'
                  ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                  : 'bg-slate-700/40 text-slate-400 border border-slate-650'
              }`}>
                {auth.priority}
              </span>
            </div>
            <p className="text-xs text-slate-400">Created on {auth.created_at || '2026-08-12'}</p>
          </div>
        </div>

        <button
          onClick={() => onNavigate('review')}
          className="py-2 px-4 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white font-medium rounded-lg text-sm shadow-lg shadow-indigo-600/20 transition-all duration-150 flex items-center gap-2 cursor-pointer"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          View Triage Recommendation
        </button>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Left Side: Clinical Summary */}
        <div className="md:col-span-2 space-y-6">
          {/* Patient Details & Status */}
          <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-6 backdrop-blur-sm shadow-md space-y-4">
            <h2 className="text-sm font-bold text-white uppercase tracking-wider border-b border-slate-700/50 pb-2">
              Clinical Context
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-xs text-slate-500 uppercase tracking-wider block">Patient ID</span>
                <span className="font-mono text-slate-200 font-semibold">{auth.patient_id}</span>
              </div>
              <div>
                <span className="text-xs text-slate-500 uppercase tracking-wider block">Current Status</span>
                <span className={`inline-flex px-2 py-0.5 rounded-full text-xs font-semibold mt-1 ${
                  auth.status === 'APPROVED'
                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                    : auth.status === 'DENIED'
                    ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                    : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                }`}>
                  {auth.status.replace('_', ' ')}
                </span>
              </div>
            </div>
          </div>

          {/* Diagnoses and Procedures */}
          <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-6 backdrop-blur-sm shadow-md space-y-4">
            <h2 className="text-sm font-bold text-white uppercase tracking-wider border-b border-slate-700/50 pb-2">
              Diagnosis & Procedure Details
            </h2>
            <div className="space-y-4 text-sm">
              <div className="flex gap-4">
                <div className="w-16 text-xs text-indigo-400 font-mono font-semibold py-1 bg-indigo-500/10 rounded border border-indigo-500/20 text-center self-start">
                  {auth.diagnosis_code}
                </div>
                <div>
                  <span className="text-xs text-slate-500 uppercase tracking-wider block">Diagnosis</span>
                  <span className="text-slate-200 font-medium">{auth.diagnosis}</span>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="w-16 text-xs text-emerald-400 font-mono font-semibold py-1 bg-emerald-500/10 rounded border border-emerald-500/20 text-center self-start">
                  CPT {auth.cpt_code}
                </div>
                <div>
                  <span className="text-xs text-slate-500 uppercase tracking-wider block">Requested Procedure</span>
                  <span className="text-slate-200 font-medium">{auth.requested_procedure}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Clinical Justification & Notes */}
          <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-6 backdrop-blur-sm shadow-md space-y-3">
            <h2 className="text-sm font-bold text-white uppercase tracking-wider border-b border-slate-700/50 pb-2">
              Clinical Notes / Justification
            </h2>
            <div className="text-slate-350 text-sm whitespace-pre-line leading-relaxed font-sans bg-slate-900/40 border border-slate-800 p-4 rounded-lg">
              {auth.clinical_notes}
            </div>
          </div>
        </div>

        {/* Right Side: Documents & Actions */}
        <div className="space-y-6">
          {/* Supporting Documents */}
          <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-6 backdrop-blur-sm shadow-md space-y-4">
            <h2 className="text-sm font-bold text-white uppercase tracking-wider border-b border-slate-700/50 pb-2">
              Attachments (Placeholder)
            </h2>
            <div className="space-y-2.5">
              {(auth.supporting_documents || []).length > 0 ? (
                auth.supporting_documents.map((doc, idx) => (
                  <div key={idx} className="flex items-center gap-2.5 p-2 bg-slate-900/60 border border-slate-800 rounded-lg text-xs hover:bg-slate-900 transition-all">
                    <svg className="w-4 h-4 text-indigo-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <span className="truncate text-slate-300 font-medium" title={doc}>
                      {doc}
                    </span>
                  </div>
                ))
              ) : (
                <div className="text-xs text-slate-500 italic p-3 bg-slate-900/20 border border-slate-800 rounded-lg text-center">
                  No supporting documents attached.
                </div>
              )}
            </div>
          </div>

          {/* Quick Review Simulation Action */}
          <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-6 backdrop-blur-sm shadow-md text-center space-y-3">
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Review Decision</h3>
            <p className="text-xs text-slate-500 leading-normal">
              Click below to view the policy evaluation matching criteria.
            </p>
            <button
              onClick={() => onNavigate('review')}
              className="w-full py-2 px-3 bg-slate-700/80 hover:bg-slate-700 hover:text-white border border-slate-600/50 hover:border-slate-500/50 rounded-lg text-xs transition-all duration-150 cursor-pointer font-medium text-slate-300"
            >
              Analyze Criteria Match
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

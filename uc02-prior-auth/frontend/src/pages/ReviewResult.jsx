import React, { useState } from 'react'

export default function ReviewResult({ auth, onNavigate, onUpdateStatus }) {
  const [decision, setDecision] = useState('APPROVE')
  const [notes, setNotes] = useState('')

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

  // Derive mock recommendation based on diagnosis or priority for demo
  const mockRecommendation = auth.priority === 'Urgent' ? 'PEND_NURSE_REVIEW' : 'APPROVE'
  const confidence = auth.priority === 'Urgent' ? '82%' : '94%'

  const handleActionSubmit = async (e) => {
    e.preventDefault()
    await onUpdateStatus(auth.id, decision)
    onNavigate('dashboard')
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3 border-b border-slate-800 pb-4">
        <button
          onClick={() => onNavigate('details')}
          className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg cursor-pointer transition-all duration-150 border border-slate-700/50"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
        </button>
        <div>
          <h1 className="text-xl font-bold text-white">Triage & Policy Evaluation</h1>
          <p className="text-xs text-slate-400">Review evaluation results and apply reviewer decisions.</p>
        </div>
      </div>

      {/* Triage Recommendation Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Recommended Action Card */}
        <div className="sm:col-span-2 p-6 bg-slate-800/40 border border-slate-700/50 rounded-xl backdrop-blur-sm shadow-md">
          <div className="text-xs font-semibold text-slate-450 uppercase tracking-wider">AI Recommended Triage Action</div>
          <div className="mt-3 flex items-center gap-3">
            <span className={`inline-flex px-3 py-1 rounded-full text-sm font-bold border ${
              mockRecommendation === 'APPROVE'
                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
            }`}>
              {mockRecommendation}
            </span>
          </div>
          <p className="mt-3 text-xs text-slate-400 leading-normal">
            Based on clinical guidelines, CPT code matches, and diagnosis codes.
          </p>
        </div>

        {/* Confidence Card */}
        <div className="p-6 bg-slate-800/40 border border-slate-700/50 rounded-xl backdrop-blur-sm shadow-md flex flex-col justify-between">
          <div>
            <div className="text-xs font-semibold text-slate-450 uppercase tracking-wider">Confidence Score</div>
            <div className="mt-2 text-3xl font-extrabold text-indigo-400">{confidence}</div>
          </div>
          <div className="text-[10px] text-slate-500 font-mono mt-2">Deterministic rules engine</div>
        </div>
      </div>

      {/* Matching Evidence Guidelines (Mocked) */}
      <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-6 backdrop-blur-sm shadow-md space-y-4">
        <h2 className="text-sm font-bold text-white uppercase tracking-wider border-b border-slate-700/50 pb-2">
          Coverage Guidelines matching (Mocked Guidelines)
        </h2>
        <div className="space-y-3">
          <div className="flex items-start gap-3 p-3 bg-slate-900/40 border border-slate-800 rounded-lg">
            <div className="p-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mt-0.5">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div>
              <span className="text-xs font-semibold text-slate-300">CPT Code Match Found</span>
              <p className="text-[11px] text-slate-450 leading-relaxed">
                CPT {auth.cpt_code} matches standard policy medical criteria requirements.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-3 bg-slate-900/40 border border-slate-800 rounded-lg">
            <div className="p-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mt-0.5">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div>
              <span className="text-xs font-semibold text-slate-300">Diagnosis Code ICD-10 Match</span>
              <p className="text-[11px] text-slate-450 leading-relaxed">
                ICD-10 code {auth.diagnosis_code} matches standard medical policy code coverage mapping.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-3 bg-slate-900/40 border border-slate-800 rounded-lg">
            <div className={`p-1 rounded mt-0.5 ${
              auth.priority === 'Urgent'
                ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
            }`}>
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                {auth.priority === 'Urgent' ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                )}
              </svg>
            </div>
            <div>
              <span className="text-xs font-semibold text-slate-300">Clinical Notes Alignment</span>
              <p className="text-[11px] text-slate-450 leading-relaxed">
                {auth.priority === 'Urgent'
                  ? 'Clinical justification indicates urgent review required due to severity reported.'
                  : 'Documented evidence of conservative management matched checklist guidelines.'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Reviewer Action Form */}
      <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-6 backdrop-blur-sm shadow-md space-y-4">
        <h2 className="text-sm font-bold text-white uppercase tracking-wider border-b border-slate-700/50 pb-2">
          Reviewer Audit Decision (Human-in-the-Loop)
        </h2>
        <form onSubmit={handleActionSubmit} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <label className="flex items-center justify-between p-3.5 bg-slate-900 border border-slate-700 rounded-lg cursor-pointer hover:border-slate-500 transition-all">
              <span className="text-xs font-semibold text-emerald-400">APPROVE</span>
              <input
                type="radio"
                name="decision"
                value="APPROVED"
                checked={decision === 'APPROVED'}
                onChange={() => setDecision('APPROVED')}
                className="w-4 h-4 text-indigo-600 border-slate-600 focus:ring-indigo-500 cursor-pointer"
              />
            </label>
            <label className="flex items-center justify-between p-3.5 bg-slate-900 border border-slate-700 rounded-lg cursor-pointer hover:border-slate-500 transition-all">
              <span className="text-xs font-semibold text-rose-400">DENY</span>
              <input
                type="radio"
                name="decision"
                value="DENIED"
                checked={decision === 'DENIED'}
                onChange={() => setDecision('DENIED')}
                className="w-4 h-4 text-indigo-600 border-slate-600 focus:ring-indigo-500 cursor-pointer"
              />
            </label>
            <label className="flex items-center justify-between p-3.5 bg-slate-900 border border-slate-700 rounded-lg cursor-pointer hover:border-slate-500 transition-all">
              <span className="text-xs font-semibold text-amber-400">PEND REVIEW</span>
              <input
                type="radio"
                name="decision"
                value="PENDING_REVIEW"
                checked={decision === 'PENDING_REVIEW'}
                onChange={() => setDecision('PENDING_REVIEW')}
                className="w-4 h-4 text-indigo-600 border-slate-600 focus:ring-indigo-500 cursor-pointer"
              />
            </label>
          </div>

          <div>
            <label htmlFor="notes" className="block text-xs font-medium text-slate-350 uppercase tracking-wider mb-1.5">
              Reviewer Notes / Comments
            </label>
            <textarea
              id="notes"
              rows="3"
              placeholder="Record notes detailing why this decision was reached..."
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 placeholder-slate-650 focus:border-indigo-500 focus:outline-none transition-all duration-150 font-sans"
            ></textarea>
          </div>

          <div className="flex justify-end gap-3 pt-3 border-t border-slate-700/50">
            <button
              type="button"
              onClick={() => onNavigate('details')}
              className="py-2 px-4 bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium rounded-lg text-sm transition-all duration-150 border border-slate-700/50 cursor-pointer"
            >
              Back to Details
            </button>
            <button
              type="submit"
              className="py-2 px-5 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white font-medium rounded-lg text-sm shadow-lg shadow-indigo-600/20 transition-all duration-150 cursor-pointer"
            >
              Submit Decision
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

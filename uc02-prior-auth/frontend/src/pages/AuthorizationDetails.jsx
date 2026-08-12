import React, { useState, useEffect } from 'react'
import { fetchPatientProfile, fetchClinicalExtraction, triggerClinicalExtraction } from '../services/api'

export default function AuthorizationDetails({ auth, onNavigate }) {
  const [activeTab, setActiveTab] = useState('request') // 'request' | 'patient' | 'ai'
  const [patientProfile, setPatientProfile] = useState(null)
  const [clinicalExtraction, setClinicalExtraction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [refreshing, setRefreshing] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (auth) {
      loadEvidenceData()
    }
  }, [auth])

  const loadEvidenceData = async () => {
    setLoading(true)
    setError('')
    
    let patientErr = ''
    let extractionErr = ''

    // 1. Fetch patient clinical profile
    try {
      const patientData = await fetchPatientProfile(auth.patient_id)
      setPatientProfile(patientData)
    } catch (err) {
      console.error('Failed to load patient profile:', err)
      patientErr = err.message || 'Connection failed'
    }

    // 2. Fetch clinical extraction (cache or triggered)
    try {
      const extractionData = await fetchClinicalExtraction(auth.id)
      setClinicalExtraction(extractionData)
    } catch (err) {
      console.error('Failed to load AI extraction:', err)
      extractionErr = err.message || 'Connection failed'
    }

    if (patientErr || extractionErr) {
      const details = []
      if (patientErr) details.push(`Patient details: ${patientErr}`)
      if (extractionErr) details.push(`AI facts: ${extractionErr}`)
      setError(`Notice: ${details.join(' • ')}`)
    } else {
      setError('')
    }
    
    setLoading(false)
  }

  const handleRefreshExtraction = async () => {
    setRefreshing(true)
    setError('')
    try {
      const refreshedData = await triggerClinicalExtraction(auth.id)
      setClinicalExtraction(refreshedData)
    } catch (err) {
      console.error('Failed to refresh AI extraction:', err)
      setError('Extraction Refresh Failed: Unable to ping the LLM. Verify OpenRouter/OpenAI status.')
    } finally {
      setRefreshing(false)
    }
  }

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
    <div className="max-w-6xl mx-auto space-y-6">
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
          Proceed to Review Decision
        </button>
      </div>

      {/* Error Alert Box */}
      {error && (
        <div className="bg-rose-500/10 border border-rose-500/20 text-rose-450 p-4 rounded-xl text-xs flex justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <svg className="w-4 h-4 text-rose-400 flex-shrink-0 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <span>{error}</span>
          </div>
          <button
            onClick={loadEvidenceData}
            className="px-2.5 py-1 bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 font-bold rounded cursor-pointer transition text-[11px]"
          >
            Retry Loading
          </button>
        </div>
      )}

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 gap-1 bg-slate-950/20 p-1 rounded-xl">
        <button
          onClick={() => setActiveTab('request')}
          className={`flex-1 sm:flex-initial py-2.5 px-5 text-xs font-semibold rounded-lg transition-all duration-150 cursor-pointer ${
            activeTab === 'request'
              ? 'bg-slate-800 text-white border border-slate-700/50 shadow-sm'
              : 'text-slate-450 hover:text-slate-350 hover:bg-slate-850/40'
          }`}
        >
          Request Details
        </button>
        <button
          onClick={() => setActiveTab('patient')}
          className={`flex-1 sm:flex-initial py-2.5 px-5 text-xs font-semibold rounded-lg transition-all duration-150 cursor-pointer flex items-center justify-center gap-1.5 ${
            activeTab === 'patient'
              ? 'bg-slate-800 text-white border border-slate-700/50 shadow-sm'
              : 'text-slate-450 hover:text-slate-350 hover:bg-slate-850/40'
          }`}
        >
          Patient Clinical History
          {patientProfile && (
            <span className="inline-flex px-1.5 py-0.5 rounded-full text-[9px] bg-indigo-500/20 text-indigo-400">
              Loaded
            </span>
          )}
        </button>
        <button
          onClick={() => setActiveTab('ai')}
          className={`flex-1 sm:flex-initial py-2.5 px-5 text-xs font-semibold rounded-lg transition-all duration-150 cursor-pointer flex items-center justify-center gap-1.5 ${
            activeTab === 'ai'
              ? 'bg-slate-800 text-white border border-slate-700/50 shadow-sm'
              : 'text-slate-450 hover:text-slate-350 hover:bg-slate-850/40'
          }`}
        >
          AI Fact Extraction
          {clinicalExtraction && (
            <span className="inline-flex px-1.5 py-0.5 rounded-full text-[9px] bg-emerald-500/20 text-emerald-400 font-mono">
              AI
            </span>
          )}
        </button>
      </div>

      {/* Tab Contents */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-24 space-y-3 bg-slate-900/30 border border-slate-800 rounded-2xl">
          <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
          <span className="text-sm text-slate-400">Loading clinical evidence profile...</span>
        </div>
      ) : (
        <div className="space-y-6">
          {/* TAB 1: REQUEST DETAILS */}
          {activeTab === 'request' && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Left Side */}
              <div className="md:col-span-2 space-y-6">
                {/* Clinical Context info */}
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

                {/* Clinical Notes */}
                <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-6 backdrop-blur-sm shadow-md space-y-3">
                  <h2 className="text-sm font-bold text-white uppercase tracking-wider border-b border-slate-700/50 pb-2">
                    Clinical Notes / Justification
                  </h2>
                  <div className="text-slate-300 text-sm whitespace-pre-line leading-relaxed font-sans bg-slate-900/40 border border-slate-800 p-4 rounded-lg">
                    {auth.clinical_notes}
                  </div>
                </div>
              </div>

              {/* Right Side */}
              <div className="space-y-6">
                {/* Supporting Documents */}
                <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-6 backdrop-blur-sm shadow-md space-y-4">
                  <h2 className="text-sm font-bold text-white uppercase tracking-wider border-b border-slate-700/50 pb-2">
                    Attachments
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
              </div>
            </div>
          )}

          {/* TAB 2: PATIENT CLINICAL HISTORY */}
          {activeTab === 'patient' && (
            <div className="space-y-6">
              {patientProfile ? (
                <>
                  {/* Patient Demographic Summary Card */}
                  <div className="bg-gradient-to-r from-slate-800/80 to-slate-850/80 border border-indigo-500/20 rounded-xl p-6 shadow-lg space-y-4">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 rounded-full bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400 text-lg font-bold">
                        {patientProfile.demographics.first_name[0]}
                        {patientProfile.demographics.last_name[0]}
                      </div>
                      <div>
                        <h2 className="text-lg font-bold text-white">
                          {patientProfile.demographics.first_name} {patientProfile.demographics.last_name}
                        </h2>
                        <p className="text-xs text-slate-400">
                          {patientProfile.demographics.gender === 'M' ? 'Male' : 'Female'} • Age: {patientProfile.demographics.age} • DOB: {patientProfile.demographics.dob}
                        </p>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs pt-4 border-t border-slate-700/50">
                      <div>
                        <span className="text-slate-500 block uppercase tracking-wider font-semibold">Insurance Plan</span>
                        <span className="text-slate-200 font-medium">{patientProfile.demographics.insurance_plan}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block uppercase tracking-wider font-semibold">Member ID</span>
                        <span className="text-slate-200 font-mono font-medium">{patientProfile.demographics.member_id}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block uppercase tracking-wider font-semibold">Patient ID</span>
                        <span className="text-slate-200 font-mono font-medium">{patientProfile.patient_id}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block uppercase tracking-wider font-semibold">Clinical Records</span>
                        <span className="text-slate-200 font-medium">
                          {(patientProfile.conditions || []).length} Conditions • {(patientProfile.medications || []).length} Medications
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Conditions & Medications Section Grid */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Active Conditions */}
                    <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-6 shadow-md space-y-3">
                      <h3 className="text-xs font-bold text-white uppercase tracking-wider border-b border-slate-700/50 pb-2 flex items-center justify-between">
                        <span>Diagnosed Conditions</span>
                        <span className="px-2 py-0.5 rounded bg-slate-700 text-[10px] text-slate-300">
                          {(patientProfile.conditions || []).length}
                        </span>
                      </h3>
                      <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
                        {(patientProfile.conditions || []).length > 0 ? (
                          patientProfile.conditions.map((cond, idx) => (
                            <div key={idx} className="p-3 bg-slate-900/40 border border-slate-800 rounded-lg flex justify-between items-start gap-4">
                              <div>
                                <span className="text-xs font-semibold text-slate-250 block">{cond.description}</span>
                                <span className="text-[10px] text-slate-500 mt-1 block">Onset: {cond.start_date || 'N/A'}</span>
                              </div>
                              <span className="px-2 py-0.5 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 text-[10px] font-mono rounded">
                                {cond.code}
                              </span>
                            </div>
                          ))
                        ) : (
                          <div className="text-xs text-slate-500 italic py-6 text-center">No active conditions.</div>
                        )}
                      </div>
                    </div>

                    {/* Medications Prescribed */}
                    <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-6 shadow-md space-y-3">
                      <h3 className="text-xs font-bold text-white uppercase tracking-wider border-b border-slate-700/50 pb-2 flex items-center justify-between">
                        <span>Medication History</span>
                        <span className="px-2 py-0.5 rounded bg-slate-700 text-[10px] text-slate-300">
                          {(patientProfile.medications || []).length}
                        </span>
                      </h3>
                      <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
                        {(patientProfile.medications || []).length > 0 ? (
                          patientProfile.medications.map((med, idx) => (
                            <div key={idx} className="p-3 bg-slate-900/40 border border-slate-800 rounded-lg flex justify-between items-start gap-4">
                              <div>
                                <span className="text-xs font-semibold text-slate-250 block">{med.description}</span>
                                <span className="text-[10px] text-slate-500 mt-1 block">Prescribed: {med.start_date || 'N/A'}</span>
                              </div>
                              <span className={`px-2 py-0.5 text-[9px] font-semibold rounded ${
                                med.status === 'active' 
                                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                                  : 'bg-slate-700/30 text-slate-400 border border-slate-650'
                              }`}>
                                {med.status || 'Active'}
                              </span>
                            </div>
                          ))
                        ) : (
                          <div className="text-xs text-slate-500 italic py-6 text-center">No medication history.</div>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Procedures & Surgeries Section Grid */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Historical Procedures */}
                    <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-6 shadow-md space-y-3">
                      <h3 className="text-xs font-bold text-white uppercase tracking-wider border-b border-slate-700/50 pb-2 flex items-center justify-between">
                        <span>Clinical Procedures</span>
                        <span className="px-2 py-0.5 rounded bg-slate-700 text-[10px] text-slate-300">
                          {(patientProfile.procedures || []).length}
                        </span>
                      </h3>
                      <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
                        {(patientProfile.procedures || []).length > 0 ? (
                          patientProfile.procedures.map((proc, idx) => (
                            <div key={idx} className="p-3 bg-slate-900/40 border border-slate-800 rounded-lg flex justify-between items-start gap-4">
                              <div>
                                <span className="text-xs font-semibold text-slate-250 block">{proc.description}</span>
                                <span className="text-[10px] text-slate-500 mt-1 block">Date completed: {proc.date || 'N/A'}</span>
                              </div>
                              <span className="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-mono rounded">
                                CPT {proc.code}
                              </span>
                            </div>
                          ))
                        ) : (
                          <div className="text-xs text-slate-500 italic py-6 text-center">No clinical procedures.</div>
                        )}
                      </div>
                    </div>

                    {/* Surgeries and Devices */}
                    <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-6 shadow-md space-y-3">
                      <h3 className="text-xs font-bold text-white uppercase tracking-wider border-b border-slate-700/50 pb-2 flex items-center justify-between">
                        <span>Surgical History</span>
                        <span className="px-2 py-0.5 rounded bg-slate-700 text-[10px] text-slate-300">
                          {(patientProfile.surgeries || []).length}
                        </span>
                      </h3>
                      <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
                        {(patientProfile.surgeries || []).length > 0 ? (
                          patientProfile.surgeries.map((surg, idx) => (
                            <div key={idx} className="p-3 bg-slate-900/40 border border-slate-800 rounded-lg">
                              <span className="text-xs font-semibold text-slate-250 block">{surg.description}</span>
                              <div className="flex justify-between items-center mt-2 text-[10px] text-slate-500">
                                <span>Date: {surg.date || 'N/A'}</span>
                                <span className="font-mono text-[9px] bg-slate-850 px-1 py-0.5 rounded">
                                  SNOMED: {surg.code}
                                </span>
                              </div>
                            </div>
                          ))
                        ) : (
                          <div className="text-xs text-slate-500 italic py-6 text-center">No surgical records.</div>
                        )}
                      </div>
                    </div>
                  </div>
                </>
              ) : (
                <div className="text-xs text-slate-500 italic p-6 bg-slate-900/20 border border-slate-800 rounded-xl text-center">
                  Patient clinical history details are unavailable.
                </div>
              )}
            </div>
          )}

          {/* TAB 3: AI FACT EXTRACTION */}
          {activeTab === 'ai' && (
            <div className="space-y-6">
              {clinicalExtraction ? (
                <>
                  {/* Extraction Metadata Banner */}
                  <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 text-xs">
                    <div className="flex items-center gap-2">
                      <svg className="w-5 h-5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <div>
                        <span className="text-slate-450 block">AI Model Configured</span>
                        <span className="font-mono text-slate-200 font-semibold">{clinicalExtraction.model}</span>
                      </div>
                    </div>
                    <div className="sm:text-right">
                      <span className="text-slate-455 block">Last Extracted</span>
                      <span className="text-slate-300 font-medium">
                        {new Date(clinicalExtraction.timestamp).toLocaleString()}
                      </span>
                    </div>
                    <button
                      onClick={handleRefreshExtraction}
                      disabled={refreshing}
                      className="py-1.5 px-3 bg-slate-750 hover:bg-slate-700 text-slate-200 border border-slate-650 hover:border-slate-550 rounded-lg text-xs transition-all flex items-center gap-1.5 font-medium cursor-pointer self-start sm:self-center disabled:opacity-50"
                    >
                      {refreshing ? (
                        <>
                          <div className="w-3.5 h-3.5 border-2 border-slate-300 border-t-transparent rounded-full animate-spin"></div>
                          Extracting...
                        </>
                      ) : (
                        <>
                          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 1121.21 7.89M9 11l3-3m0 0l3 3m-3-3v12" />
                          </svg>
                          Re-run AI Extractor
                        </>
                      )}
                    </button>
                  </div>

                  {/* Fact Extraction Card details */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Key Metrics details */}
                    <div className="md:col-span-2 space-y-6">
                      <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-6 shadow-md space-y-5">
                        <h3 className="text-xs font-bold text-white uppercase tracking-wider border-b border-slate-700/50 pb-2">
                          AI-Extracted Clinical Metrics
                        </h3>

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                          {/* Symptom Duration */}
                          <div className="p-4 bg-slate-900/40 border border-slate-800 rounded-lg flex flex-col justify-between">
                            <div>
                              <span className="text-slate-500 block uppercase tracking-wider text-[10px] font-semibold">
                                Symptom Duration
                              </span>
                              <span className="text-[11px] text-slate-400 block mt-0.5">
                                Documented timeline of complaints
                              </span>
                            </div>
                            <div className="mt-3.5">
                              {clinicalExtraction.structured_extraction.symptom_duration_weeks !== null ? (
                                <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 text-sm font-bold rounded-lg">
                                  {clinicalExtraction.structured_extraction.symptom_duration_weeks} Weeks
                                </span>
                              ) : (
                                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 bg-slate-700/30 text-slate-500 border border-slate-650 text-xs rounded font-medium">
                                  Unspecified / Null
                                </span>
                              )}
                            </div>
                          </div>

                          {/* Physiotherapy Duration */}
                          <div className="p-4 bg-slate-900/40 border border-slate-800 rounded-lg flex flex-col justify-between">
                            <div>
                              <span className="text-slate-500 block uppercase tracking-wider text-[10px] font-semibold">
                                Physiotherapy Completed
                              </span>
                              <span className="text-[11px] text-slate-400 block mt-0.5">
                                Conservative physical therapy duration
                              </span>
                            </div>
                            <div className="mt-3.5">
                              {clinicalExtraction.structured_extraction.physiotherapy_weeks !== null ? (
                                <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-sm font-bold rounded-lg">
                                  {clinicalExtraction.structured_extraction.physiotherapy_weeks} Weeks
                                </span>
                              ) : (
                                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 bg-slate-700/30 text-slate-500 border border-slate-650 text-xs rounded font-medium">
                                  Unspecified / Null
                                </span>
                              )}
                            </div>
                          </div>
                        </div>

                        {/* Medications and Imaging */}
                        <div className="space-y-4 pt-2">
                          {/* Attempted Medications */}
                          <div>
                            <span className="text-slate-500 uppercase tracking-wider text-[10px] font-semibold block mb-2">
                              Conservative Medications Attempted
                            </span>
                            <div className="flex flex-wrap gap-2">
                              {(clinicalExtraction.structured_extraction.medications_attempted || []).length > 0 ? (
                                clinicalExtraction.structured_extraction.medications_attempted.map((med, idx) => (
                                  <span key={idx} className="px-2.5 py-1 bg-slate-900 text-slate-200 border border-slate-750 text-xs rounded-lg font-medium shadow-sm">
                                    {med}
                                  </span>
                                ))
                              ) : (
                                <span className="text-xs text-slate-500 italic p-2 bg-slate-900/20 border border-slate-850 rounded-lg block w-full">
                                  No attempted medications explicitly documented in the note.
                                </span>
                              )}
                            </div>
                          </div>

                          {/* Previous Imaging */}
                          <div>
                            <span className="text-slate-500 uppercase tracking-wider text-[10px] font-semibold block mb-2">
                              Prior Imaging / Diagnostics Done
                            </span>
                            <div className="flex flex-wrap gap-2">
                              {(clinicalExtraction.structured_extraction.previous_imaging || []).length > 0 ? (
                                clinicalExtraction.structured_extraction.previous_imaging.map((img, idx) => (
                                  <span key={idx} className="px-2.5 py-1 bg-slate-900 text-slate-200 border border-slate-750 text-xs rounded-lg font-medium shadow-sm">
                                    {img}
                                  </span>
                                ))
                              ) : (
                                <span className="text-xs text-slate-500 italic p-2 bg-slate-900/20 border border-slate-850 rounded-lg block w-full">
                                  No historical imaging/scans documented in the note.
                                </span>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Right side: Missing/Unknown fields */}
                    <div className="space-y-6">
                      <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-6 shadow-md space-y-4">
                        <h3 className="text-xs font-bold text-white uppercase tracking-wider border-b border-slate-700/50 pb-2">
                          Unspecified Parameters (Unknown Fields)
                        </h3>

                        <div className="space-y-2">
                          {(clinicalExtraction.structured_extraction.unknown_fields || []).length > 0 ? (
                            clinicalExtraction.structured_extraction.unknown_fields.map((field, idx) => (
                              <div key={idx} className="flex items-center gap-2 p-2.5 bg-rose-500/5 border border-rose-500/10 text-rose-350 text-xs rounded-lg">
                                <svg className="w-4 h-4 text-rose-450 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                                <span className="font-medium truncate" title={field}>
                                  {field.replace(/_/g, ' ')}
                                </span>
                              </div>
                            ))
                          ) : (
                            <div className="text-xs text-emerald-400 font-semibold p-3.5 bg-emerald-500/5 border border-emerald-500/10 rounded-lg text-center">
                              No unspecified clinical criteria flagged. Note is fully descriptive!
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </>
              ) : (
                <div className="text-xs text-slate-500 italic p-6 bg-slate-900/20 border border-slate-800 rounded-xl text-center">
                  AI clinical extraction details are unavailable.
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

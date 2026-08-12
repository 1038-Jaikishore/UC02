import React, { useState } from 'react'

export default function NewAuthorization({ onNavigate, onAddAuthorization }) {
  const [formData, setFormData] = useState({
    patient_id: '',
    diagnosis: '',
    diagnosis_code: '',
    requested_procedure: '',
    cpt_code: '',
    clinical_notes: '',
    priority: 'Standard'
  })
  const [error, setError] = useState('')

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    
    // Simple frontend validations
    if (!formData.patient_id || !formData.diagnosis || !formData.diagnosis_code || !formData.requested_procedure || !formData.cpt_code || !formData.clinical_notes) {
      setError('Please fill in all clinical and patient details.')
      return
    }

    setError('')
    
    // Call the parent handler to update state
    onAddAuthorization(formData)
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {/* Header */}
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
          <h1 className="text-xl font-bold text-white">New Prior Authorization Request</h1>
          <p className="text-xs text-slate-400">Submit clinical details for automated triage processing.</p>
        </div>
      </div>

      {/* Form Card */}
      <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-8 backdrop-blur-sm shadow-xl space-y-6">
        {error && (
          <div className="p-3 bg-rose-500/10 border border-rose-500/20 text-rose-400 rounded-lg text-xs font-medium">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Patient ID and Priority */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label htmlFor="patient_id" className="block text-xs font-medium text-slate-350 uppercase tracking-wider mb-1.5">
                Patient ID
              </label>
              <input
                type="text"
                id="patient_id"
                name="patient_id"
                placeholder="e.g. PT-1002"
                value={formData.patient_id}
                onChange={handleChange}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 placeholder-slate-650 focus:border-indigo-500 focus:outline-none transition-all duration-150"
              />
            </div>
            <div>
              <label htmlFor="priority" className="block text-xs font-medium text-slate-350 uppercase tracking-wider mb-1.5">
                Priority
              </label>
              <select
                id="priority"
                name="priority"
                value={formData.priority}
                onChange={handleChange}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none transition-all duration-150 cursor-pointer"
              >
                <option value="Standard">Standard</option>
                <option value="Urgent">Urgent</option>
              </select>
            </div>
          </div>

          {/* Diagnosis & Diagnosis Code */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="sm:col-span-2">
              <label htmlFor="diagnosis" className="block text-xs font-medium text-slate-350 uppercase tracking-wider mb-1.5">
                Diagnosis Description
              </label>
              <input
                type="text"
                id="diagnosis"
                name="diagnosis"
                placeholder="e.g. Primary Osteoarthritis, Right Knee"
                value={formData.diagnosis}
                onChange={handleChange}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 placeholder-slate-650 focus:border-indigo-500 focus:outline-none transition-all duration-150"
              />
            </div>
            <div>
              <label htmlFor="diagnosis_code" className="block text-xs font-medium text-slate-350 uppercase tracking-wider mb-1.5">
                Diagnosis ICD-10 Code
              </label>
              <input
                type="text"
                id="diagnosis_code"
                name="diagnosis_code"
                placeholder="e.g. M17.11"
                value={formData.diagnosis_code}
                onChange={handleChange}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 placeholder-slate-650 focus:border-indigo-500 focus:outline-none transition-all duration-150"
              />
            </div>
          </div>

          {/* Procedure & CPT Code */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="sm:col-span-2">
              <label htmlFor="requested_procedure" className="block text-xs font-medium text-slate-350 uppercase tracking-wider mb-1.5">
                Requested Procedure
              </label>
              <input
                type="text"
                id="requested_procedure"
                name="requested_procedure"
                placeholder="e.g. Arthroplasty, Knee, Condyle and Patella"
                value={formData.requested_procedure}
                onChange={handleChange}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 placeholder-slate-650 focus:border-indigo-500 focus:outline-none transition-all duration-150"
              />
            </div>
            <div>
              <label htmlFor="cpt_code" className="block text-xs font-medium text-slate-350 uppercase tracking-wider mb-1.5">
                CPT Procedure Code
              </label>
              <input
                type="text"
                id="cpt_code"
                name="cpt_code"
                placeholder="e.g. 27447"
                value={formData.cpt_code}
                onChange={handleChange}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 placeholder-slate-650 focus:border-indigo-500 focus:outline-none transition-all duration-150"
              />
            </div>
          </div>

          {/* Clinical Notes */}
          <div>
            <label htmlFor="clinical_notes" className="block text-xs font-medium text-slate-350 uppercase tracking-wider mb-1.5">
              Clinical Justification & Notes
            </label>
            <textarea
              id="clinical_notes"
              name="clinical_notes"
              rows="4"
              placeholder="Provide symptoms, conservative therapy results, pain score, functional limitations, diagnostic testing results (MRI, X-ray), etc."
              value={formData.clinical_notes}
              onChange={handleChange}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 placeholder-slate-650 focus:border-indigo-500 focus:outline-none transition-all duration-150 font-sans"
            ></textarea>
          </div>

          {/* Supporting Documents Upload Placeholder */}
          <div>
            <label className="block text-xs font-medium text-slate-350 uppercase tracking-wider mb-1.5">
              Supporting Documentation (Placeholder)
            </label>
            <div className="border-2 border-dashed border-slate-700 rounded-lg p-6 text-center bg-slate-900/40 hover:bg-slate-900/60 transition-all duration-150">
              <svg className="w-8 h-8 text-slate-500 mx-auto mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <span className="block text-xs text-slate-400 font-medium">Drag and drop files here, or click to upload</span>
              <span className="block text-[10px] text-slate-500 mt-1">PDF, PNG, JPG, or DICOM files (mock attachment)</span>
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-end gap-3 pt-3 border-t border-slate-700/50">
            <button
              type="button"
              onClick={() => onNavigate('dashboard')}
              className="py-2.5 px-4 bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium rounded-lg text-sm transition-all duration-150 border border-slate-700/50 cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="py-2.5 px-5 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white font-medium rounded-lg text-sm shadow-lg shadow-indigo-600/20 transition-all duration-150 cursor-pointer"
            >
              Submit Request
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

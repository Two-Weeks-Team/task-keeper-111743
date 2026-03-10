import { useState } from 'react';

export default function SyncSettings() {
  const [enabled, setEnabled] = useState(false);
  const [keyVisible, setKeyVisible] = useState(false);

  return (
    <section className="mt-8 p-4 bg-gray-800 rounded">
      <h2 className="text-2xl font-semibold mb-4">Zero‑Knowledge Sync</h2>
      <div className="flex items-center mb-2">
        <label className="mr-2">Sync Enabled:</label>
        <input
          type="checkbox"
          checked={enabled}
          onChange={(e) => setEnabled(e.target.checked)}
          className="form-checkbox h-5 w-5 text-blue-600"
        />
      </div>
      {enabled && (
        <div className="mt-4">
          <p className="text-sm text-gray-400 mb-2">
            Your encryption key never leaves this device. Keep it safe!
          </p>
          <button
            onClick={() => setKeyVisible((v) => !v)}
            className="px-3 py-1 bg-gray-700 rounded hover:bg-gray-600"
          >
            {keyVisible ? 'Hide' : 'Show'} Encryption Key
          </button>
          {keyVisible && (
            <pre className="mt-2 p-2 bg-gray-900 rounded text-xs break-all">
              {/* Placeholder – in a real app the key would be derived from user credentials */}
              01234567‑89ab‑cdef‑0123‑456789abcdef
            </pre>
          )}
        </div>
      )}
    </section>
  );
}

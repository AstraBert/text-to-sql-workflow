"use client"

import { useWorkflowHandler } from "@llamaindex/ui";

export default function HandlerDetails({ handlerId }: { handlerId: string | null }) {
  // Note, the state will remain empty if the handler ID is empty
  const { handler, events, sendEvent } = useWorkflowHandler(handlerId ?? "", true);

  // Find the final StopEvent to extract the workflow result (if provided)
  const stop = events.find(
    (e) =>
      e.type.endsWith(
        "StopEvent"
      ) || e.type.endsWith(
        "OutputEvent" // handle text-to-sql-specific case
      ) /* event type contains the event's full Python module path, e.g., workflows.events.StopEvent */
  );
  if (handler) {
    return (
        <div className="mt-6 bg-gray-900 border border-gray-700 rounded-lg p-4 space-y-4">
        <div className="flex items-center gap-3">
            <strong className="text-white font-semibold">{handler.handler_id}</strong>
            <span className="text-gray-400">—</span>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
            handler.status === 'complete' ? 'bg-green-900/50 text-green-300' :
            handler.status === 'running' ? 'bg-blue-900/50 text-blue-300' :
            handler.status === 'failed' ? 'bg-red-900/50 text-red-300' :
            'bg-gray-800 text-gray-300'
            }`}>
            {handler.status}
            </span>
        </div>
        
        {stop ? (
            <pre className="bg-black/50 border border-gray-800 rounded-lg p-4 text-gray-100 text-sm overflow-x-auto">
            {JSON.stringify(stop.data, null, 2)}
            </pre>
        ) : (
            <pre className="bg-black/50 border border-gray-800 rounded-lg p-4 text-gray-100 text-sm overflow-auto max-h-60">
            {JSON.stringify(events, null, 2)}
            </pre>
        )}
        </div>
    );
    } else {
    return (
        <div className="mt-6 bg-gray-900 border border-red-900/50 rounded-lg p-4">
        <div className="flex items-center gap-2 text-red-400">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <strong className="font-semibold">
            {`Handler with handler ID: ${handlerId} not found`}
            </strong>
        </div>
        </div>
    );
    }
}
"use client"

import { ChangeEvent, useState } from "react";
import { useWorkflowRun } from "@llamaindex/ui";
import HandlerDetails from "./handler-details";

export default function RunButton() {
  const { runWorkflow, isCreating, error } = useWorkflowRun();
  const [handlerId, setHandlerId] = useState<string | null>(null);
  const [dbUri, setDBUri] = useState<string | null>(null)
  const [message, setMessage] = useState<string | null>(null)
  const [useTls, setUseTls] = useState<boolean>(false)

  async function handleMessageChange(e: ChangeEvent<HTMLInputElement>) {
    setMessage(e.target.value)
  }

  async function handleDbUriChange(e: ChangeEvent<HTMLInputElement>) {
    setDBUri(e.target.value)
  }

  async function handleClick() {
    const handler = await runWorkflow("text-to-sql-workflow", { message: message, db_uri: dbUri, enable_tls: useTls });
    console.log("Started:", handler.handler_id);
    setHandlerId(handler.handler_id);
  }

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6">
  <div className="space-y-2">
    <label className="block text-sm font-medium text-white">
      Your Text-To-SQL message:
    </label>
    <input
      type="text"
      placeholder="Type what you want to know about your database..."
      onChange={handleMessageChange}
      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
    />
  </div>

  <div className="space-y-2">
    <label className="block text-sm font-medium text-white">
      Database Connection URI:
    </label>
    <input
      type="password"
      placeholder="postgresql://user:password@host:port/database"
      onChange={handleDbUriChange}
      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition font-mono text-sm"
    />
  </div>

  <div className="flex items-center space-x-3">
    <input
      type="checkbox"
      checked={useTls}
      onChange={(e) => setUseTls(e.target.checked)}
      className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
    />
    <label className="text-sm font-medium text-white">
      Enable TLS?
    </label>
  </div>

  <button
    disabled={isCreating}
    onClick={handleClick}
    className="w-full px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
  >
    {isCreating ? "Starting…" : "Run Workflow"}
  </button>

  <HandlerDetails handlerId={handlerId} />
</div>
  );
}
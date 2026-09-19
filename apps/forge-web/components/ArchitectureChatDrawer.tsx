'use client';

import React, { useState } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatDrawerProps {
  analysisResult: any;
}

export default function ArchitectureChatDrawer({ analysisResult }: ChatDrawerProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! I am your ONGISA Architecture Assistant. Ask me anything about your dependency tree, code smells, or validation structures.' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: userMsg }]);
    setLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: userMsg, codebase_context: analysisResult }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { role: 'assistant', content: data.answer || data.error }]);
    } catch {
      setMessages((prev) => [...prev, { role: 'assistant', content: 'Error connecting to ONGISA AI backend service.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Floating Toggle Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 z-40 bg-cyan-600 hover:bg-cyan-500 text-white px-4 py-3 rounded-full shadow-2xl flex items-center gap-2 font-medium text-sm transition"
      >
        <span>💬</span> Ask ONGISA AI
      </button>

      {/* Slide-over Drawer */}
      {isOpen && (
        <div className="fixed inset-y-0 right-0 z-50 w-full max-w-md bg-gray-900 border-l border-gray-800 shadow-2xl flex flex-col">
          <div className="p-4 border-b border-gray-800 flex justify-between items-center bg-gray-950">
            <h2 className="text-sm font-bold text-cyan-400 uppercase tracking-wider">
              Architecture AI Assistant
            </h2>
            <button
              onClick={() => setIsOpen(false)}
              className="text-gray-400 hover:text-white font-bold text-lg"
            >
              ✕
            </button>
          </div>

          <div className="flex-1 p-4 overflow-y-auto space-y-4 font-mono text-xs">
            {messages.map((m, idx) => (
              <div
                key={idx}
                className={`p-3 rounded-lg ${
                  m.role === 'user'
                    ? 'bg-cyan-950/40 border border-cyan-800/50 text-cyan-200 ml-6'
                    : 'bg-gray-950 border border-gray-800 text-gray-300 mr-6'
                }`}
              >
                <span className="block font-bold text-[10px] uppercase text-gray-500 mb-1">
                  {m.role === 'user' ? 'You' : 'ONGISA AI'}
                </span>
                <p className="whitespace-pre-wrap leading-relaxed">{m.content}</p>
              </div>
            ))}
            {loading && (
              <div className="p-3 bg-gray-950 border border-gray-800 text-gray-500 italic rounded-lg mr-6">
                Thinking...
              </div>
            )}
          </div>

          <form onSubmit={handleSend} className="p-4 border-t border-gray-800 bg-gray-950 flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="e.g. Where is data validation handled?"
              className="flex-1 bg-gray-900 border border-gray-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500 font-mono"
            />
            <button
              type="submit"
              disabled={loading}
              className="bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white px-4 py-2 rounded-lg text-xs font-semibold transition"
            >
              Send
            </button>
          </form>
        </div>
      )}
    </>
  );
}
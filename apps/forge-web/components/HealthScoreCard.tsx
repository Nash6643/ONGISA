import React from 'react';

export const HealthScoreCard = ({ score }: { score: number }) => {
  return (
    <div className="p-4 border rounded-xl bg-slate-900 text-white shadow-md">
      <h3 className="text-sm font-semibold text-slate-400">Code Health Index</h3>
      <p className="text-3xl font-bold mt-2 text-emerald-400">{score} / 100</p>
    </div>
  );
};
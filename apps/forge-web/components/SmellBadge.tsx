import React from 'react';

interface SmellBadgeProps {
  severity: 'high' | 'medium' | 'low';
}

export default function SmellBadge({ severity }: SmellBadgeProps) {
  const styles = {
    high: 'bg-red-950/80 text-red-400 border-red-900',
    medium: 'bg-amber-950/80 text-amber-400 border-amber-900',
    low: 'bg-blue-950/80 text-blue-400 border-blue-900',
  };

  return (
    <span className={`px-2.5 py-0.5 text-xs font-mono border rounded uppercase ${styles[severity] || styles.low}`}>
      {severity}
    </span>
  );
}
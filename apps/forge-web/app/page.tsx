import DependencyGraph from '@/components/DependencyGraph';

export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto space-y-6">
        <header className="border-b border-gray-800 pb-4">
          <h1 className="text-3xl font-bold tracking-tight text-white">
            Forge Architecture Dashboard
          </h1>
          <p className="text-sm text-gray-400 mt-1">
            Visualizing dependency graphs, symbol trees, and refactoring insights.
          </p>
        </header>
        <DependencyGraph />
      </div>
    </main>
  );
}
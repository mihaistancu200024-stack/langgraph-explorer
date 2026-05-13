import { useEffect, useState } from 'react'
import { getGraphs } from './api/client'
import { GraphSidebar } from './components/GraphSidebar'
import { GraphRunner } from './components/GraphRunner'
import type { GraphMeta } from './types'

export function App() {
  const [graphs, setGraphs] = useState<GraphMeta[]>([])
  const [selectedGraph, setSelectedGraph] = useState<GraphMeta | null>(null)

  useEffect(() => {
    getGraphs()
      .then(data => setGraphs(data))
      .catch(err => console.error('Failed to load graphs:', err))
  }, [])

  return (
    <div style={{ display: 'flex', flexDirection: 'row', height: '100vh', overflow: 'hidden' }}>
      <div
        style={{
          width: 260,
          minWidth: 260,
          background: '#f3f2f1',
          padding: '16px 8px',
          overflowY: 'auto',
          borderRight: '1px solid #e1dfdd',
        }}
      >
        <GraphSidebar
          graphs={graphs}
          selected={selectedGraph}
          onSelect={setSelectedGraph}
        />
      </div>
      <div style={{ flex: 1, overflowY: 'auto', padding: 24 }}>
        {selectedGraph ? (
          <GraphRunner graph={selectedGraph} />
        ) : (
          <div style={{ color: '#605e5c', marginTop: 48, textAlign: 'center' }}>
            Select a graph from the sidebar to get started.
          </div>
        )}
      </div>
    </div>
  )
}

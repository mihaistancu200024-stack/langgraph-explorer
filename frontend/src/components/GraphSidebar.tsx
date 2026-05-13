import { Button, Title3 } from '@fluentui/react-components'
import type { GraphMeta } from '../types'

interface GraphSidebarProps {
  graphs: GraphMeta[]
  selected: GraphMeta | null
  onSelect: (g: GraphMeta) => void
}

export function GraphSidebar({ graphs, selected, onSelect }: GraphSidebarProps) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
      <Title3 style={{ marginBottom: 12, paddingLeft: 8 }}>LangGraph Explorer</Title3>
      {graphs.map(graph => (
        <Button
          key={graph.id}
          appearance={selected?.id === graph.id ? 'primary' : 'subtle'}
          onClick={() => onSelect(graph)}
          style={{
            justifyContent: 'flex-start',
            textAlign: 'left',
            width: '100%',
            padding: '8px 12px',
          }}
        >
          {graph.name}
        </Button>
      ))}
      {graphs.length === 0 && (
        <div style={{ color: '#605e5c', fontSize: 13, padding: '8px 12px' }}>
          Loading graphs...
        </div>
      )}
    </div>
  )
}

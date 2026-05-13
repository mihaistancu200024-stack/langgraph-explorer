import mermaid from 'mermaid'
import { useEffect, useRef, useState } from 'react'
import { getDiagram } from '../api/client'

mermaid.initialize({ startOnLoad: false, theme: 'neutral' })

export function GraphDiagram({ graphId }: { graphId: string }) {
  const ref = useRef<HTMLDivElement>(null)
  const [svg, setSvg] = useState('')
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setSvg('')
    setError(null)
    getDiagram(graphId)
      .then(async code => {
        try {
          // Use a unique id per render to avoid mermaid caching issues
          const uniqueId = `graph-diagram-${graphId}-${Date.now()}`
          const { svg: rendered } = await mermaid.render(uniqueId, code)
          setSvg(rendered)
        } catch (renderErr) {
          console.error('Mermaid render error:', renderErr)
          setError('Failed to render diagram.')
        }
      })
      .catch(fetchErr => {
        console.error('Failed to fetch diagram:', fetchErr)
        setError('Failed to load diagram.')
      })
  }, [graphId])

  if (error) {
    return (
      <div style={{ marginTop: 16, color: '#a4262c', fontSize: 13 }}>
        {error}
      </div>
    )
  }

  if (!svg) {
    return (
      <div style={{ marginTop: 16, color: '#605e5c', fontSize: 13 }}>
        Loading diagram...
      </div>
    )
  }

  return (
    <div
      ref={ref}
      dangerouslySetInnerHTML={{ __html: svg }}
      style={{ marginTop: 16, overflowX: 'auto' }}
    />
  )
}

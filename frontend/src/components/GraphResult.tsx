import { Card, CardHeader, Title3 } from '@fluentui/react-components'

interface GraphResultProps {
  result: object | null
}

export function GraphResult({ result }: GraphResultProps) {
  if (result === null) return null

  return (
    <Card style={{ marginTop: 16 }}>
      <CardHeader header={<Title3>Result</Title3>} />
      <pre
        style={{
          margin: '8px 0 0 0',
          padding: '12px 16px',
          background: '#f3f2f1',
          borderRadius: 4,
          fontSize: 13,
          overflowX: 'auto',
          whiteSpace: 'pre-wrap',
          wordBreak: 'break-word',
        }}
      >
        {JSON.stringify(result, null, 2)}
      </pre>
    </Card>
  )
}

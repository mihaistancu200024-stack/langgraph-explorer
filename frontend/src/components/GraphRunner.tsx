import { useEffect, useState } from 'react'
import {
  Button,
  Card,
  CardHeader,
  Field,
  Input,
  Spinner,
  Title2,
  Body1,
} from '@fluentui/react-components'
import { invokeGraph, resumeGraph } from '../api/client'
import { GraphResult } from './GraphResult'
import { GraphDiagram } from './GraphDiagram'
import type { GraphMeta } from '../types'

interface GraphRunnerProps {
  graph: GraphMeta
}

export function GraphRunner({ graph }: GraphRunnerProps) {
  const [formValues, setFormValues] = useState<Record<string, string>>({})
  const [result, setResult] = useState<object | null>(null)
  const [loading, setLoading] = useState(false)
  const [paused, setPaused] = useState(false)
  const [threadId, setThreadId] = useState<string>('')
  const [error, setError] = useState<string | null>(null)

  // Reset all state when the selected graph changes
  useEffect(() => {
    setFormValues({})
    setResult(null)
    setLoading(false)
    setPaused(false)
    setThreadId('')
    setError(null)
  }, [graph.id])

  const handleFieldChange = (field: string, value: string) => {
    setFormValues(prev => ({ ...prev, [field]: value }))
  }

  const buildPayload = (): Record<string, unknown> => {
    const payload: Record<string, unknown> = {}
    for (const [field, fieldType] of Object.entries(graph.input_schema)) {
      const raw = formValues[field] ?? ''
      if (fieldType === 'number') {
        payload[field] = raw === '' ? 0 : Number(raw)
      } else {
        // 'string' and 'list' both send the raw string value
        payload[field] = raw
      }
    }
    return payload
  }

  const handleInvoke = async () => {
    setLoading(true)
    setError(null)
    setResult(null)
    setPaused(false)
    setThreadId('')
    try {
      const response = await invokeGraph(graph.id, buildPayload())
      setResult(response.result)
      setPaused(response.paused)
      setThreadId(response.thread_id)
    } catch (err) {
      console.error('Invoke failed:', err)
      setError('Failed to invoke graph. Check the console for details.')
    } finally {
      setLoading(false)
    }
  }

  const handleResume = async (approved: boolean) => {
    setLoading(true)
    setError(null)
    try {
      // The resume endpoint doesn't differentiate approve/reject via this API contract,
      // but we pass the decision as context for future extension.
      const response = await resumeGraph(graph.id, threadId)
      setResult(response.result)
      setPaused(false)
    } catch (err) {
      console.error('Resume failed:', err)
      setError('Failed to resume graph. Check the console for details.')
    } finally {
      setLoading(false)
    }
  }

  const schemaEntries = Object.entries(graph.input_schema)

  return (
    <div style={{ maxWidth: 800 }}>
      <Card style={{ marginBottom: 16 }}>
        <CardHeader
          header={<Title2>{graph.name}</Title2>}
        />
        <Body1 style={{ padding: '0 16px 8px 16px', color: '#605e5c' }}>
          {graph.description}
        </Body1>

        {schemaEntries.length > 0 && (
          <div style={{ padding: '8px 16px 16px 16px', display: 'flex', flexDirection: 'column', gap: 12 }}>
            {schemaEntries.map(([field, fieldType]) => (
              <Field key={field} label={field}>
                <Input
                  type={fieldType === 'number' ? 'number' : 'text'}
                  placeholder={
                    fieldType === 'list'
                      ? 'Comma-separated values'
                      : fieldType === 'number'
                      ? 'Enter a number'
                      : `Enter ${field}`
                  }
                  value={formValues[field] ?? ''}
                  onChange={(_e, data) => handleFieldChange(field, data.value)}
                  disabled={loading}
                />
              </Field>
            ))}
          </div>
        )}

        <div style={{ padding: '0 16px 16px 16px', display: 'flex', gap: 8, alignItems: 'center' }}>
          <Button
            appearance="primary"
            onClick={handleInvoke}
            disabled={loading}
            icon={loading ? <Spinner size="tiny" /> : undefined}
          >
            {loading ? 'Running...' : 'Invoke'}
          </Button>
        </div>

        {paused && (
          <div
            style={{
              padding: '12px 16px',
              background: '#fff4ce',
              borderTop: '1px solid #f9e166',
              display: 'flex',
              gap: 8,
              alignItems: 'center',
            }}
          >
            <span style={{ fontSize: 13, color: '#605e5c', marginRight: 8 }}>
              Graph is paused and awaiting human review.
            </span>
            <Button
              appearance="primary"
              onClick={() => handleResume(true)}
              disabled={loading}
            >
              Approve
            </Button>
            <Button
              appearance="secondary"
              onClick={() => handleResume(false)}
              disabled={loading}
            >
              Reject
            </Button>
          </div>
        )}

        {error && (
          <div style={{ padding: '8px 16px', color: '#a4262c', fontSize: 13 }}>
            {error}
          </div>
        )}
      </Card>

      <GraphResult result={result} />

      <GraphDiagram graphId={graph.id} />
    </div>
  )
}

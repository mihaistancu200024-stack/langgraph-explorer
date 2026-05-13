export interface GraphMeta {
  id: string
  name: string
  description: string
  input_schema: Record<string, 'string' | 'number' | 'list'>
}

export interface InvokeResult {
  result: object
  paused: boolean
  thread_id: string
}

export interface ResumeResult {
  result: object
}

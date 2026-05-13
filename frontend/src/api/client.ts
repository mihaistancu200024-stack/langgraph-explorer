import axios from 'axios'
import type { GraphMeta, InvokeResult, ResumeResult } from '../types'

const BASE = 'http://localhost:8000'

export const getGraphs = (): Promise<GraphMeta[]> =>
  axios.get(`${BASE}/api/graphs`).then(r => r.data)

export const getDiagram = (id: string): Promise<string> =>
  axios.get(`${BASE}/api/graphs/${id}/diagram`).then(r => r.data.mermaid)

export const invokeGraph = (id: string, body: Record<string, unknown>): Promise<InvokeResult> =>
  axios.post(`${BASE}/api/graphs/${id}/invoke`, body).then(r => r.data)

export const resumeGraph = (id: string, threadId: string): Promise<ResumeResult> =>
  axios.post(`${BASE}/api/graphs/${id}/resume`, { thread_id: threadId }).then(r => r.data)

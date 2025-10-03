/**
 * 全局类型定义
 */

export interface User {
  id: string
  name: string
  avatar?: string
  email?: string
}

export interface Session {
  id: string
  docId: string
  messages: ChatMessage[]
  currentArticle: string
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp?: string
}



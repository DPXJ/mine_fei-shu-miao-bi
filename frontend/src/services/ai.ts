/**
 * AI创作服务
 */
import axios from 'axios'
import { authService } from './auth'
import { ContentBlock } from './documents'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface Message {
  role: 'user' | 'assistant'
  content: string
}

export interface AIResponse {
  session_id: string
  content: string
  messages: Message[]
}

class AIService {
  private getHeaders() {
    const token = authService.getToken()
    return {
      Authorization: `Bearer ${token}`,
    }
  }

  /**
   * 首次生成文章
   */
  async createArticle(
    docId: string,
    blocks: ContentBlock[],
    instruction: string
  ): Promise<AIResponse> {
    const response = await axios.post(
      `${API_URL}/api/ai/create`,
      {
        doc_id: docId,
        blocks,
        instruction,
      },
      {
        headers: this.getHeaders(),
      }
    )
    return response.data
  }

  /**
   * 精修文章
   */
  async refineArticle(
    sessionId: string,
    instruction: string
  ): Promise<AIResponse> {
    const response = await axios.post(
      `${API_URL}/api/ai/refine`,
      {
        session_id: sessionId,
        instruction,
      },
      {
        headers: this.getHeaders(),
      }
    )
    return response.data
  }

  /**
   * 重置会话
   */
  async resetSession(sessionId: string): Promise<void> {
    await axios.delete(`${API_URL}/api/ai/session/${sessionId}`, {
      headers: this.getHeaders(),
    })
  }

  /**
   * 获取会话信息
   */
  async getSession(sessionId: string): Promise<any> {
    const response = await axios.get(
      `${API_URL}/api/ai/session/${sessionId}`,
      {
        headers: this.getHeaders(),
      }
    )
    return response.data
  }

  /**
   * 预览重新排版后的文章（包含图片）
   */
  async previewArticle(sessionId: string): Promise<{
    session_id: string
    doc_id: string
    article_content: string
    images: Array<{mime_type: string; data: string}>
    original_blocks: ContentBlock[]
  }> {
    const response = await axios.get(
      `${API_URL}/api/ai/preview/${sessionId}`,
      {
        headers: this.getHeaders(),
      }
    )
    return response.data
  }
}

export const aiService = new AIService()



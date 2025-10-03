/**
 * 文档服务
 */
import axios from 'axios'
import { authService } from './auth'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface Document {
  doc_id: string
  title: string
  doc_type: string
  updated_at: string
  url: string
}

export interface ContentBlock {
  block_id: string
  block_type: string
  text?: string
  image_token?: string
  image_url?: string
}

export interface DocumentContent {
  doc_id: string
  title: string
  blocks: ContentBlock[]
}

class DocumentService {
  private getHeaders() {
    const token = authService.getToken()
    return {
      Authorization: `Bearer ${token}`,
    }
  }

  /**
   * 获取文档列表
   */
  async getDocuments(pageSize: number = 20): Promise<Document[]> {
    const response = await axios.get(`${API_URL}/api/documents/list`, {
      headers: this.getHeaders(),
      params: { page_size: pageSize, order_by: 'EditedTime', direction: 'Desc' },
    })
    return response.data.documents
  }

  /**
   * 获取文档内容
   */
  async getDocumentContent(docId: string): Promise<DocumentContent> {
    const response = await axios.get(
      `${API_URL}/api/documents/content/${docId}`,
      {
        headers: this.getHeaders(),
      }
    )
    return response.data
  }

  /**
   * 获取图片URL
   */
  getImageUrl(docId: string, imageToken: string): string {
    const token = authService.getToken()
    return `${API_URL}/api/documents/image/${docId}/${imageToken}?token=${token}`
  }
}

export const documentService = new DocumentService()



/**
 * 后端API服务
 * 复用现有的 backend_py FastAPI 服务
 */

// 后端地址 - 根据实际情况修改
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

interface GenerateRequest {
  texts: string;
  images: string[];
  instruction: string;
}

interface GenerateResponse {
  session_id: string;
  content: string;
  messages: any[];
}

/**
 * 调用后端AI生成接口
 */
export async function generateArticle(request: GenerateRequest): Promise<GenerateResponse> {
  try {
    const response = await fetch(`${BACKEND_URL}/api/ai/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        doc_id: 'widget_doc', // 小组件固定ID
        blocks: [
          {
            type: 'text',
            text: request.texts
          },
          ...request.images.map(token => ({
            type: 'image',
            token: token
          }))
        ],
        instruction: request.instruction
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || '生成失败');
    }

    const result = await response.json();
    return result;
  } catch (error: any) {
    console.error('API调用失败:', error);
    throw new Error(error.message || '网络请求失败');
  }
}
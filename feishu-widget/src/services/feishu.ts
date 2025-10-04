/**
 * 飞书SDK服务
 * 封装飞书文档操作相关功能
 */

import { docx } from '@lark-base-open/js-sdk';

export interface FeishuBlock {
  block_id: string;
  block_type: number;
  text?: {
    elements: Array<{
      text_run?: {
        content: string;
      };
    }>;
  };
  image?: {
    token: string;
  };
}

export interface DocumentContent {
  texts: string[];
  images: string[];
  blocks: FeishuBlock[];
}

/**
 * 读取当前文档的所有内容
 */
export async function readDocumentContent(): Promise<DocumentContent> {
  try {
    // 获取文档的所有blocks
    const blocks = await docx.getBlocks();
    
    const texts: string[] = [];
    const images: string[] = [];
    
    // 解析blocks
    for (const block of blocks) {
      if (block.block_type === 1 || block.block_type === 2 || 
          block.block_type === 4 || block.block_type === 5) {
        // 文本块类型
        const textContent = extractTextFromBlock(block);
        if (textContent.trim()) {
          texts.push(textContent);
        }
      } else if (block.block_type === 27) {
        // 图片块
        if (block.image?.token) {
          images.push(block.image.token);
        }
      }
    }
    
    return {
      texts,
      images,
      blocks
    };
  } catch (error) {
    console.error('读取文档失败:', error);
    throw new Error('读取文档内容失败，请检查权限设置');
  }
}

/**
 * 从文本块中提取文本内容
 */
function extractTextFromBlock(block: FeishuBlock): string {
  if (!block.text?.elements) {
    return '';
  }
  
  return block.text.elements
    .map(element => element.text_run?.content || '')
    .join('');
}

/**
 * 插入文本内容到文档
 */
export async function insertTextContent(content: string, position: 'start' | 'end' = 'end'): Promise<void> {
  try {
    // 将markdown内容转换为飞书blocks格式
    const blocks = convertMarkdownToBlocks(content);
    
    // 插入blocks
    for (const block of blocks) {
      await docx.insertBlock({
        block_type: block.block_type,
        ...block.data,
        position: position
      });
    }
  } catch (error) {
    console.error('插入内容失败:', error);
    throw new Error('插入内容失败，请重试');
  }
}

/**
 * 插入图片到文档
 */
export async function insertImage(imageToken: string, position: 'start' | 'end' = 'end'): Promise<void> {
  try {
    await docx.insertBlock({
      block_type: 27, // 图片类型
      image: {
        token: imageToken
      },
      position: position
    });
  } catch (error) {
    console.error('插入图片失败:', error);
    throw new Error('插入图片失败，请重试');
  }
}

/**
 * 将Markdown内容转换为飞书blocks格式
 */
function convertMarkdownToBlocks(content: string): Array<{
  block_type: number;
  data: any;
}> {
  const lines = content.split('\n');
  const blocks: Array<{ block_type: number; data: any }> = [];
  
  for (const line of lines) {
    const trimmedLine = line.trim();
    if (!trimmedLine) continue;
    
    // 检查标题
    if (trimmedLine.startsWith('####')) {
      blocks.push({
        block_type: 5, // 三级标题
        data: {
          heading3: {
            elements: [{
              text_run: {
                content: trimmedLine.substring(4).trim()
              }
            }]
          }
        }
      });
    } else if (trimmedLine.startsWith('###')) {
      blocks.push({
        block_type: 5, // 三级标题
        data: {
          heading3: {
            elements: [{
              text_run: {
                content: trimmedLine.substring(3).trim()
              }
            }]
          }
        }
      });
    } else if (trimmedLine.startsWith('##')) {
      blocks.push({
        block_type: 4, // 二级标题
        data: {
          heading2: {
            elements: [{
              text_run: {
                content: trimmedLine.substring(2).trim()
              }
            }]
          }
        }
      });
    } else if (trimmedLine.startsWith('#')) {
      blocks.push({
        block_type: 3, // 一级标题
        data: {
          heading1: {
            elements: [{
              text_run: {
                content: trimmedLine.substring(1).trim()
              }
            }]
          }
        }
      });
    } else {
      // 普通文本
      blocks.push({
        block_type: 2, // 文本块
        data: {
          text: {
            elements: [{
              text_run: {
                content: trimmedLine
              }
            }]
          }
        }
      });
    }
  }
  
  return blocks;
}

/**
 * 获取当前文档信息
 */
export async function getDocumentInfo(): Promise<{
  title: string;
  doc_id: string;
}> {
  try {
    const docInfo = await docx.getDocument();
    return {
      title: docInfo.title || '未命名文档',
      doc_id: docInfo.document_id
    };
  } catch (error) {
    console.error('获取文档信息失败:', error);
    return {
      title: '未知文档',
      doc_id: 'unknown'
    };
  }
}

/**
 * 检查是否在飞书环境中
 */
export function isInFeishuEnvironment(): boolean {
  return typeof window !== 'undefined' && 
         window.location.hostname.includes('feishu.cn');
}

/**
 * 开发模式下的模拟数据
 */
export function getMockDocumentContent(): DocumentContent {
  return {
    texts: [
      '# 测试文档标题',
      '这是一段测试内容，用于演示AI文档助手的功能。',
      'GitHub配机子,还有Couplate WeFly、腾讯库和阿里云。',
      '## 二级标题',
      '这里是一些示例文本，展示多级标题的效果。'
    ],
    images: ['mock_image_token_1', 'mock_image_token_2'],
    blocks: []
  };
}

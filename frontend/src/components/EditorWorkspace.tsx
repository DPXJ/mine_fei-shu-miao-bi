'use client'

import { useState, useEffect } from 'react'
import {
  Layout,
  Card,
  Input,
  Button,
  Spin,
  message,
  Typography,
  Space,
  Divider,
  Image,
  Empty,
  Modal,
} from 'antd'
import {
  ArrowLeftOutlined,
  SendOutlined,
  ReloadOutlined,
  CopyOutlined,
  FileImageOutlined,
  FileAddOutlined,
} from '@ant-design/icons'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { documentService, Document, ContentBlock } from '@/services/documents'
import { aiService, Message } from '@/services/ai'

const { Sider, Content } = Layout
const { TextArea } = Input
const { Title, Text, Paragraph } = Typography

interface Props {
  document: Document
  onBack: () => void
}

export default function EditorWorkspace({ document, onBack }: Props) {
  const [blocks, setBlocks] = useState<ContentBlock[]>([])
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)
  const [instruction, setInstruction] = useState('')
  const [article, setArticle] = useState('')
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [showPreview, setShowPreview] = useState(false)
  const [previewImages, setPreviewImages] = useState<Array<{mime_type: string; data: string}>>([])

  useEffect(() => {
    loadContent()
  }, [document])

  const loadContent = async () => {
    try {
      setLoading(true)
      const content = await documentService.getDocumentContent(document.doc_id)
      console.log('Document content loaded:', content)
      console.log('Blocks:', content.blocks)
      console.log('Text blocks:', content.blocks.filter(block => block.block_type === 'text'))
      console.log('Image blocks:', content.blocks.filter(block => block.block_type === 'image'))
      setBlocks(content.blocks)
    } catch (error: any) {
      // 确保错误消息是字符串
      const errorMessage = error.response?.data?.detail?.message || 
                         error.response?.data?.detail || 
                         error.message || 
                         '加载文档内容失败'
      message.error(`加载文档内容失败：${errorMessage}`)
    } finally {
      setLoading(false)
    }
  }

  const handleGenerate = async () => {
    console.log('Generate button clicked!')
    console.log('Instruction:', instruction)
    console.log('Blocks:', blocks)
    
    if (!instruction.trim()) {
      message.warning('请输入创作指令')
      return
    }

    try {
      setGenerating(true)
      console.log('Starting AI generation...')
      
      if (!sessionId) {
        // 首次生成
        console.log('First time generation, calling createArticle...')
        const response = await aiService.createArticle(
          document.doc_id,
          blocks,
          instruction
        )
        console.log('AI response received:', response)
        setArticle(response.content)
        setSessionId(response.session_id)
        setMessages(response.messages)
        
        // 首次生成后，自动加载预览数据（包含图片）
        try {
          const previewData = await aiService.previewArticle(response.session_id)
          setPreviewImages(previewData.images)
          console.log(`Loaded ${previewData.images.length} images for preview`)
        } catch (err) {
          console.error('加载图片失败:', err)
        }
        
        message.success('文章生成成功！')
      } else {
        // 精修
        const response = await aiService.refineArticle(sessionId, instruction)
        setArticle(response.content)
        setMessages(response.messages)
        
        // 精修后也刷新预览数据
        try {
          const previewData = await aiService.previewArticle(sessionId)
          setPreviewImages(previewData.images)
        } catch (err) {
          console.error('加载图片失败:', err)
        }
        
        message.success('文章已更新！')
      }
      
      setInstruction('')
    } catch (error: any) {
      // 确保错误消息是字符串
      const errorMessage = error.response?.data?.detail?.message || 
                         error.response?.data?.detail || 
                         error.message || 
                         '生成失败'
      message.error(`生成失败：${errorMessage}`)
    } finally {
      setGenerating(false)
    }
  }

  const handleReset = async () => {
    if (sessionId) {
      try {
        await aiService.resetSession(sessionId)
      } catch (error) {
        console.error('重置会话失败', error)
      }
    }
    setSessionId(null)
    setArticle('')
    setMessages([])
    setInstruction('')
    message.info('已重置会话')
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(article)
    message.success('已复制到剪贴板')
  }

  const handleCreateFeishuCopy = async () => {
    if (!article) {
      message.warning('请先生成文章')
      return
    }

    try {
      setLoading(true)
      message.loading({ content: '正在创建飞书文档...', key: 'creating', duration: 0 })
      
      // 创建飞书文档
      const result = await documentService.createFeishuCopy(
        `${document.title} - AI创作副本`,
        article,
        previewImages || []
      )
      
      message.success({ content: '飞书文档创建成功！', key: 'creating', duration: 2 })
      
      // 显示成功提示和链接
      Modal.success({
        title: '飞书文档创建成功',
        content: (
          <div>
            <p>文档已创建成功！</p>
            <a href={result.doc_url} target="_blank" rel="noopener noreferrer" className="text-blue-500 underline">
              点击打开飞书文档
            </a>
          </div>
        ),
        okText: '知道了'
      })
    } catch (error: any) {
      message.error({ content: `创建失败：${error.response?.data?.detail || error.message}`, key: 'creating' })
    } finally {
      setLoading(false)
    }
  }

  const handlePreview = async () => {
    if (!sessionId) {
      message.warning('请先生成文章')
      return
    }

    try {
      setLoading(true)
      const previewData = await aiService.previewArticle(sessionId)
      setPreviewImages(previewData.images)
      setArticle(previewData.article_content)
      setShowPreview(true)
      message.success('预览加载成功')
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.message || '加载预览失败'
      message.error(`加载预览失败：${errorMessage}`)
    } finally {
      setLoading(false)
    }
  }

  // 渲染文章内容，将 ![alt](image_N) 替换为实际图片
  const renderArticleWithImages = (content: string) => {
    console.log('renderArticleWithImages called')
    console.log('previewImages:', previewImages)
    console.log('content length:', content?.length)
    
    if (!previewImages || previewImages.length === 0) {
      console.log('No preview images, rendering markdown as-is')
      return <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
    }

    // 替换图片占位符为实际的base64图片
    let renderedContent = content
    previewImages.forEach((img, index) => {
      const placeholderRegex = new RegExp(`!\\[([^\\]]*)\\]\\(image_${index + 1}\\)`, 'g')
      const imgTag = `![${img.mime_type}](data:${img.mime_type};base64,${img.data})`
      console.log(`Replacing image_${index + 1} with base64 data (length: ${img.data?.length})`)
      renderedContent = renderedContent.replace(placeholderRegex, imgTag)
    })

    console.log('Final rendered content length:', renderedContent.length)
    return <ReactMarkdown remarkPlugins={[remarkGfm]}>{renderedContent}</ReactMarkdown>
  }

  return (
    <Layout className="h-full">
      {/* 左侧素材栏 */}
      <Sider width={350} className="bg-white border-r overflow-y-auto" style={{ height: 'calc(100vh - 64px)' }}>
        <div className="p-4">
          <Button icon={<ArrowLeftOutlined />} onClick={onBack} className="mb-4">
            返回列表
          </Button>
          
          <Title level={5} className="!mb-2">
            素材内容
          </Title>
          <Text type="secondary" className="text-sm">
            来自: {document.title}
          </Text>
          
          <Divider />

          {loading ? (
            <div className="text-center py-8">
              <Spin />
            </div>
          ) : (
            <Space direction="vertical" size="middle" className="w-full">
              {blocks.map((block, index) => (
                <Card key={block.block_id} size="small" className="shadow-sm">
                  {block.block_type === 'text' ? (
                    <Paragraph className="!mb-0 text-sm" ellipsis={{ rows: 3, expandable: true }}>
                      {block.text}
                    </Paragraph>
                  ) : block.block_type === 'image' && block.image_token ? (
                    <div>
                      <div className="flex items-center gap-2 mb-2">
                        <FileImageOutlined />
                        <Text type="secondary" className="text-xs">
                          图片 #{index + 1}
                        </Text>
                      </div>
                      <Image
                        src={documentService.getImageUrl(document.doc_id, block.image_token)}
                        alt={`Image ${index}`}
                        className="rounded"
                      />
                    </div>
                  ) : null}
                </Card>
              ))}
            </Space>
          )}
        </div>
      </Sider>

      {/* 右侧创作区 */}
      <Content className="flex flex-col bg-gray-50" style={{ height: 'calc(100vh - 64px)' }}>
        {/* 文档内容预览区 */}
        <div className="bg-white border-b p-4 max-h-64 overflow-y-auto">
          <Title level={5} className="!mb-3">文档内容预览</Title>
          {blocks.length > 0 ? (
            <div className="space-y-3">
              {blocks.map((block, index) => (
                <div key={block.block_id} className="border rounded p-3 bg-gray-50">
                  {block.block_type === 'text' ? (
                    <div>
                      <Text type="secondary" className="text-xs mb-1 block">
                        文本块 #{index + 1}
                      </Text>
                      <Paragraph className="!mb-0 text-sm">
                        {block.text || '（无文本内容）'}
                      </Paragraph>
                    </div>
                  ) : block.block_type === 'image' ? (
                    <div>
                      <Text type="secondary" className="text-xs mb-1 block">
                        图片块 #{index + 1}
                      </Text>
                      <div className="flex items-center gap-2">
                        <FileImageOutlined />
                        <Text type="secondary" className="text-xs">
                          图片已加载
                        </Text>
                      </div>
                    </div>
                  ) : (
                    <Text type="secondary" className="text-xs">
                      未知块类型: {block.block_type}
                    </Text>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <Empty
              description="暂无文档内容"
              image={Empty.PRESENTED_IMAGE_SIMPLE}
            />
          )}
        </div>

        <div className="flex-1 overflow-y-auto p-6">
          {article ? (
            <Card className="max-w-4xl mx-auto">
              <div className="flex justify-between items-center mb-4">
                <Title level={4} className="!mb-0">
                  📄 生成的文章
                </Title>
                <Space>
                  <Button 
                    type="primary"
                    icon={<FileAddOutlined />} 
                    onClick={handleCreateFeishuCopy}
                    loading={loading}
                  >
                    创建飞书副本
                  </Button>
                  <Button icon={<CopyOutlined />} onClick={handleCopy}>
                    复制
                  </Button>
                  <Button icon={<ReloadOutlined />} onClick={handleReset}>
                    重置
                  </Button>
                </Space>
              </div>
              <Divider />
              <div className="markdown-body prose max-w-none">
                {previewImages && previewImages.length > 0 && (
                  <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6">
                    <Text strong>💡 提示：</Text>
                    <div className="mt-2 text-sm">
                      <p>✅ AI已分析图片内容，并智能地将图片插入到最合适的位置</p>
                      <p>✅ 图片与文本内容协同排版，逻辑连贯</p>
                      <p>✅ 文档中包含 {previewImages.length} 张图片</p>
                    </div>
                  </div>
                )}
                {renderArticleWithImages(article)}
              </div>
            </Card>
          ) : (
            <div className="h-full flex items-center justify-center">
              <Empty
                description="输入创作指令，开始生成文章"
                image={Empty.PRESENTED_IMAGE_SIMPLE}
              />
            </div>
          )}
        </div>

        {/* 对话区 */}
        <div className="border-t bg-white p-4">
          <div className="max-w-4xl mx-auto">
            {messages.length > 0 && (
              <div className="mb-4 max-h-32 overflow-y-auto">
                <Space direction="vertical" size="small" className="w-full">
                  {messages.map((msg, index) => (
                    <div
                      key={index}
                      className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`px-3 py-2 rounded-lg max-w-md ${
                          msg.role === 'user'
                            ? 'bg-blue-500 text-white'
                            : 'bg-gray-200 text-gray-800'
                        }`}
                      >
                        <Text className={msg.role === 'user' ? 'text-white' : ''}>
                          {msg.content}
                        </Text>
                      </div>
                    </div>
                  ))}
                </Space>
              </div>
            )}

            <div className="flex gap-2">
              <TextArea
                placeholder={
                  sessionId
                    ? '输入修改指令，例如："第二段太啰嗦了，帮我精简一下"'
                    : '输入创作指令，例如："帮我把这篇文章改写得更具吸引力"'
                }
                value={instruction}
                onChange={(e) => setInstruction(e.target.value)}
                onPressEnter={(e) => {
                  if (e.shiftKey) return
                  e.preventDefault()
                  handleGenerate()
                }}
                autoSize={{ minRows: 2, maxRows: 4 }}
                disabled={generating}
              />
              <Button
                type="primary"
                icon={<SendOutlined />}
                onClick={handleGenerate}
                loading={generating}
                size="large"
              >
                {sessionId ? '发送' : '生成'}
              </Button>
            </div>
            <Text type="secondary" className="text-xs mt-2 block">
              {sessionId ? '继续与AI对话，精修您的文章' : '按 Enter 发送，Shift + Enter 换行'}
            </Text>
          </div>
        </div>
      </Content>
    </Layout>
  )
}



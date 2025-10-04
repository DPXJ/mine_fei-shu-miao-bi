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
} from 'antd'
import {
  ArrowLeftOutlined,
  SendOutlined,
  ReloadOutlined,
  CopyOutlined,
  FileImageOutlined,
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
        message.success('文章生成成功！')
      } else {
        // 精修
        const response = await aiService.refineArticle(sessionId, instruction)
        setArticle(response.content)
        setMessages(response.messages)
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
                  生成的文章
                </Title>
                <Space>
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
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {article}
                </ReactMarkdown>
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



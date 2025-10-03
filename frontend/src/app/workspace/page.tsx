'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Layout, Menu, Button, Card, List, Input, message, Spin, Avatar, Typography } from 'antd'
import {
  FileTextOutlined,
  LogoutOutlined,
  SearchOutlined,
  UserOutlined,
} from '@ant-design/icons'
import { authService } from '@/services/auth'
import { documentService, Document } from '@/services/documents'
import EditorWorkspace from '@/components/EditorWorkspace'

const { Header, Sider, Content } = Layout
const { Search } = Input
const { Title, Text } = Typography

export default function WorkspacePage() {
  const router = useRouter()
  const [documents, setDocuments] = useState<Document[]>([])
  const [filteredDocs, setFilteredDocs] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedDoc, setSelectedDoc] = useState<Document | null>(null)
  const [userInfo, setUserInfo] = useState<any>(null)

  useEffect(() => {
    // 检查登录状态
    if (!authService.isAuthenticated()) {
      router.push('/')
      return
    }

    const user = authService.getUserInfo()
    setUserInfo(user)

    // 加载文档列表
    loadDocuments()
  }, [router])

  const loadDocuments = async () => {
    try {
      setLoading(true)
      const docs = await documentService.getDocuments()
      setDocuments(docs)
      setFilteredDocs(docs)
    } catch (error: any) {
      message.error('加载文档失败：' + (error.response?.data?.detail || error.message))
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (value: string) => {
    if (!value.trim()) {
      setFilteredDocs(documents)
    } else {
      const filtered = documents.filter((doc) =>
        doc.title.toLowerCase().includes(value.toLowerCase())
      )
      setFilteredDocs(filtered)
    }
  }

  const handleLogout = () => {
    authService.logout()
    message.success('已退出登录')
    router.push('/')
  }

  const handleDocumentSelect = (doc: Document) => {
    setSelectedDoc(doc)
  }

  const handleBack = () => {
    setSelectedDoc(null)
  }

  return (
    <Layout className="min-h-screen">
      <Header className="bg-white shadow-sm flex items-center justify-between px-6">
        <div className="flex items-center">
          <Title level={3} className="!mb-0 !mr-6">
            🖋️ 飞书妙笔
          </Title>
        </div>
        <div className="flex items-center gap-4">
          {userInfo && (
            <div className="flex items-center gap-2">
              <Avatar icon={<UserOutlined />} />
              <Text>{userInfo.name || '用户'}</Text>
            </div>
          )}
          <Button icon={<LogoutOutlined />} onClick={handleLogout}>
            退出
          </Button>
        </div>
      </Header>

      <Layout>
        {!selectedDoc ? (
          <Content className="p-6 bg-gray-50">
            <Card className="max-w-5xl mx-auto">
              <div className="mb-4">
                <Title level={4}>我的文档</Title>
                <Search
                  placeholder="搜索文档标题..."
                  allowClear
                  enterButton={<SearchOutlined />}
                  size="large"
                  onSearch={handleSearch}
                  onChange={(e) => handleSearch(e.target.value)}
                />
              </div>

              {loading ? (
                <div className="text-center py-12">
                  <Spin size="large" />
                  <p className="mt-4 text-gray-500">加载文档列表中...</p>
                </div>
              ) : filteredDocs.length === 0 ? (
                <div className="text-center py-12 text-gray-400">
                  <FileTextOutlined className="text-6xl mb-4" />
                  <p>暂无文档</p>
                </div>
              ) : (
                <List
                  dataSource={filteredDocs}
                  renderItem={(doc) => (
                    <List.Item
                      key={doc.doc_id}
                      className="cursor-pointer hover:bg-gray-50 transition-colors px-4 rounded"
                      onClick={() => handleDocumentSelect(doc)}
                    >
                      <List.Item.Meta
                        avatar={<FileTextOutlined className="text-2xl text-blue-500" />}
                        title={<Text strong>{doc.title}</Text>}
                        description={
                          <Text type="secondary">
                            更新时间: {new Date(parseInt(doc.updated_at)).toLocaleString('zh-CN')}
                          </Text>
                        }
                      />
                      <Button type="link">打开 →</Button>
                    </List.Item>
                  )}
                />
              )}
            </Card>
          </Content>
        ) : (
          <EditorWorkspace document={selectedDoc} onBack={handleBack} />
        )}
      </Layout>
    </Layout>
  )
}



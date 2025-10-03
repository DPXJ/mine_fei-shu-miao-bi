'use client'

import { useEffect } from 'react'
import { Button, Card, Typography } from 'antd'
import { FileTextOutlined, RobotOutlined, ThunderboltOutlined } from '@ant-design/icons'
import { useRouter } from 'next/navigation'
import { authService } from '@/services/auth'

const { Title, Paragraph } = Typography

export default function HomePage() {
  const router = useRouter()

  useEffect(() => {
    // 检查是否已登录
    const token = authService.getToken()
    if (token) {
      router.push('/workspace')
    }
  }, [router])

  const handleLogin = async () => {
    try {
      const url = await authService.getAuthUrl()
      window.location.href = url
    } catch (error) {
      console.error('获取授权链接失败:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full">
        <div className="text-center mb-12">
          <Title level={1} className="!text-5xl !mb-4">
            🖋️ 飞书妙笔
          </Title>
          <Paragraph className="text-xl text-gray-600">
            将飞书文档草稿转化为结构清晰、图文并茂的专业文章
          </Paragraph>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <Card className="text-center hover:shadow-lg transition-shadow">
            <FileTextOutlined className="text-4xl text-blue-500 mb-4" />
            <Title level={4}>智能解析</Title>
            <Paragraph className="text-gray-600">
              自动提取飞书文档中的文字和图片素材
            </Paragraph>
          </Card>

          <Card className="text-center hover:shadow-lg transition-shadow">
            <RobotOutlined className="text-4xl text-green-500 mb-4" />
            <Title level={4}>AI创作</Title>
            <Paragraph className="text-gray-600">
              基于Google Gemini的智能内容重组和润色
            </Paragraph>
          </Card>

          <Card className="text-center hover:shadow-lg transition-shadow">
            <ThunderboltOutlined className="text-4xl text-purple-500 mb-4" />
            <Title level={4}>多轮精修</Title>
            <Paragraph className="text-gray-600">
              通过对话持续优化，打造完美文章
            </Paragraph>
          </Card>
        </div>

        <div className="text-center">
          <Button
            type="primary"
            size="large"
            onClick={handleLogin}
            className="h-12 px-8 text-lg"
          >
            通过飞书登录
          </Button>
          <div className="mt-4 text-gray-500 text-sm">
            首次使用需要授权访问您的飞书文档
          </div>
        </div>

        <div className="mt-16 text-center text-gray-400 text-sm">
          <Paragraph>
            技术支持：飞书开放平台 × Google Gemini AI
          </Paragraph>
        </div>
      </div>
    </div>
  )
}



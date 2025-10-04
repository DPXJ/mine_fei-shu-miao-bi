'use client'

import { useEffect, Suspense } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { Spin, message } from 'antd'
import { authService } from '@/services/auth'

function CallbackContent() {
  const router = useRouter()
  const searchParams = useSearchParams()

  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get('code')
      
      if (!code) {
        message.error('授权失败：未获取到授权码')
        router.push('/')
        return
      }

      try {
        await authService.exchangeToken(code)
        message.success('登录成功！')
        router.push('/workspace')
      } catch (error: any) {
        console.error('Token exchange failed:', error)
        // 确保错误消息是字符串
        const errorMessage = error.response?.data?.detail?.message || 
                           error.response?.data?.detail || 
                           error.message || 
                           '登录失败，请重试'
        message.error(`登录失败：${errorMessage}`)
        router.push('/')
      }
    }

    handleCallback()
  }, [searchParams, router])

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <Spin size="large" />
        <p className="mt-4 text-gray-600">正在登录中...</p>
      </div>
    </div>
  )
}

export default function CallbackPage() {
  return (
    <Suspense fallback={<div className="min-h-screen flex items-center justify-center"><Spin size="large" /></div>}>
      <CallbackContent />
    </Suspense>
  )
}



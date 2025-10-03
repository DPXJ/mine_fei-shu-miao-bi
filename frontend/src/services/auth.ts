/**
 * 认证服务
 */
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

class AuthService {
  private TOKEN_KEY = 'feishu_access_token'
  private USER_KEY = 'feishu_user_info'

  /**
   * 获取OAuth授权URL
   */
  async getAuthUrl(): Promise<string> {
    const response = await axios.get(`${API_URL}/api/auth/url`)
    return response.data.auth_url
  }

  /**
   * 使用授权码换取token
   */
  async exchangeToken(code: string) {
    const response = await axios.post(`${API_URL}/api/auth/token`, { code })
    const { access_token, user_info } = response.data
    
    // 保存到localStorage
    this.setToken(access_token)
    this.setUserInfo(user_info)
    
    return response.data
  }

  /**
   * 保存token
   */
  setToken(token: string) {
    if (typeof window !== 'undefined') {
      localStorage.setItem(this.TOKEN_KEY, token)
    }
  }

  /**
   * 获取token
   */
  getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(this.TOKEN_KEY)
    }
    return null
  }

  /**
   * 保存用户信息
   */
  setUserInfo(userInfo: any) {
    if (typeof window !== 'undefined') {
      localStorage.setItem(this.USER_KEY, JSON.stringify(userInfo))
    }
  }

  /**
   * 获取用户信息
   */
  getUserInfo(): any {
    if (typeof window !== 'undefined') {
      const info = localStorage.getItem(this.USER_KEY)
      return info ? JSON.parse(info) : null
    }
    return null
  }

  /**
   * 退出登录
   */
  logout() {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(this.TOKEN_KEY)
      localStorage.removeItem(this.USER_KEY)
    }
  }

  /**
   * 检查是否已登录
   */
  isAuthenticated(): boolean {
    return !!this.getToken()
  }
}

export const authService = new AuthService()



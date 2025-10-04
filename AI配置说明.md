# AI提供商配置说明

## 🤖 支持的AI提供商

本项目支持两种AI提供商：

### 1. Google Gemini（默认）
- ✅ 功能强大，效果优秀
- ❌ 国内需要VPN才能访问
- 🔑 API Key获取：https://makersuite.google.com/app/apikey

### 2. DeepSeek（推荐国内用户）
- ✅ 国内可直接访问，无需VPN
- ✅ 速度快，稳定性好
- ✅ 价格实惠
- 🔑 API Key获取：https://platform.deepseek.com

## 📝 配置方法

### 方法一：使用Gemini（需要VPN）

1. **获取API Key**：
   - 访问：https://makersuite.google.com/app/apikey
   - 创建或选择项目
   - 点击"Create API Key"

2. **配置环境变量**（`backend_py/.env`）：
   ```
   GEMINI_API_KEY=你的Gemini_API_Key
   AI_PROVIDER=gemini
   ```

3. **开启VPN后启动项目**

### 方法二：使用DeepSeek（推荐）

1. **获取API Key**：
   - 访问：https://platform.deepseek.com
   - 注册/登录账号
   - 进入API管理页面
   - 创建API Key

2. **配置环境变量**（`backend_py/.env`）：
   ```
   DEEPSEEK_API_KEY=你的DeepSeek_API_Key
   AI_PROVIDER=deepseek
   ```

3. **直接启动项目**（无需VPN）

## 🔄 切换AI提供商

只需修改 `backend_py/.env` 文件中的 `AI_PROVIDER` 参数：

```env
# 使用Gemini
AI_PROVIDER=gemini
GEMINI_API_KEY=你的key

# 或使用DeepSeek
AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=你的key
```

修改后重启后端服务即可。

## ⚠️ 常见问题

### 1. Gemini API超时
**症状：** 点击"生成"按钮后一直转圈，30秒后显示超时

**原因：**
- 国内无法直接访问Gemini API
- 网络连接问题

**解决方案：**
- 开启VPN后重试
- 或切换到DeepSeek

### 2. DeepSeek API错误
**症状：** 提示"API Key无效"或其他错误

**解决方案：**
- 检查API Key是否正确
- 确认账户余额是否充足
- 查看DeepSeek官网是否有服务公告

### 3. 两个AI提供商对比

| 特性 | Gemini | DeepSeek |
|------|--------|----------|
| 国内访问 | 需要VPN | 直接访问 |
| 响应速度 | 较慢（跨境） | 快 |
| 效果质量 | 优秀 | 优秀 |
| 价格 | 有免费额度 | 按量计费 |
| 稳定性 | 中（取决于VPN） | 高 |
| 推荐场景 | 海外用户 | 国内用户 |

## 📞 技术支持

如遇到其他问题，请查看后端日志：
- Windows: 直接运行 `启动后端.bat` 可看到日志
- 或查看终端输出的详细错误信息


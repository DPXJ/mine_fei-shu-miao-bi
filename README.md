# 飞书妙笔 (Lark Artisan)

一款智能内容创作辅助应用，帮助您将飞书文档中的草稿转化为结构清晰、图文并茂的专业文章。

## 🚀 快速导航

| 如果你想... | 请看这里 |
|------------|---------|
| 💨 **快速开始使用** | [快速开始.md](./快速开始.md) - 一分钟上手 |
| 🔧 **配置环境** | [配置指南.md](./配置指南.md) - 详细配置步骤 |
| ⚡ **立即启动** | [部署前检查.md](./部署前检查.md) - 启动前检查清单 |
| 📖 **学习如何使用** | [使用演示.md](./使用演示.md) - 功能演示和案例 |
| 🏗️ **了解项目架构** | [项目结构.md](./项目结构.md) - 代码结构说明 |
| 📦 **查看交付内容** | [项目交付说明.md](./项目交付说明.md) - 完整交付文档 |

## 功能特点

- ✨ 飞书OAuth登录授权
- 📄 读取和管理飞书文档
- 🤖 AI智能内容创作（基于Google Gemini）
- 💬 多轮对话精修文章
- 🖼️ 智能图文混排
- 📤 支持导出Markdown

## 技术栈

### 前端
- Next.js 14 (React)
- TypeScript
- Ant Design + Tailwind CSS
- Axios

### 后端
- Python 3.10+
- FastAPI
- Google Gemini 1.5 Pro API
- 飞书开放平台API

## 快速开始

### 前置要求

- Node.js 18+
- Python 3.10+
- 飞书开放平台应用（App ID & App Secret）
- Google Gemini API Key

### 配置环境变量

1. 后端配置：在 `backend_py` 目录创建 `.env` 文件：

```env
# 飞书应用配置
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
FEISHU_REDIRECT_URI=http://localhost:3000/auth/callback

# Google Gemini配置
GEMINI_API_KEY=your_gemini_api_key

# 服务配置
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

2. 前端配置：在 `frontend` 目录创建 `.env.local` 文件：

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 启动项目

#### 方式一：使用启动脚本（推荐）

**Windows:**
```bash
.\启动项目.bat
```

**PowerShell:**
```powershell
.\start_all.ps1
```

#### 方式二：手动启动

**启动后端:**
```bash
cd backend_py
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python main.py
```

**启动前端:**
```bash
cd frontend
npm install
npm run dev
```

### 访问应用

打开浏览器访问: [http://localhost:3000](http://localhost:3000)

## 飞书应用配置指南

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 配置应用权限：
   - `docx:document` - 查看、评论和编辑文档
   - `drive:drive` - 查看、评论、编辑和管理云空间中的文件
4. 配置重定向URL：`http://localhost:3000/auth/callback`
5. 获取 App ID 和 App Secret

## 项目结构

```
01-飞书文档图文AI创作/
├── frontend/              # Next.js前端应用
│   ├── src/
│   │   ├── app/          # App Router页面
│   │   ├── components/   # React组件
│   │   ├── services/     # API服务
│   │   └── types/        # TypeScript类型定义
│   └── package.json
├── backend_py/           # FastAPI后端服务
│   ├── main.py          # 主入口
│   ├── routers/         # API路由
│   ├── services/        # 业务逻辑
│   └── requirements.txt
└── README.md
```

## 📖 完整文档

- 📘 [快速开始指南](./快速开始.md) - 一分钟快速上手
- 📗 [配置指南](./配置指南.md) - 详细的环境配置步骤
- 📙 [使用演示](./使用演示.md) - 功能演示和实际案例
- 📕 [项目结构](./项目结构.md) - 代码架构说明
- 📔 [开发检查清单](./开发检查清单.md) - 开发测试指南
- 📓 [版本历史](./版本历史.md) - 版本更新记录
- 📰 [项目交付说明](./项目交付说明.md) - 完整交付文档

## 🎯 核心特性

### 1. 智能内容解析
- 自动提取飞书文档中的文字段落
- 智能识别并下载图片素材
- 清晰的双栏布局展示

### 2. AI对话式创作
- 基于Google Gemini 1.5 Pro
- 支持自定义创作指令
- 智能理解上下文

### 3. 多轮迭代精修
- 保持完整对话历史
- 上下文感知的修改
- 实时预览更新

### 4. 简单易用
- 一键飞书登录
- 直观的操作界面
- 快速复制导出

## 📸 功能演示

### 创作流程
```
选择文档 → 查看素材 → 输入指令 → AI生成 → 多轮精修 → 导出使用
```

### 示例指令
- "帮我把这篇文章改写得更专业"
- "重新组织内容，突出三个核心观点"
- "第二段太啰嗦了，帮我精简一下"
- "结尾加一个总结，用三点式列出要点"

## 🔧 常见问题

### Q: 如何获取飞书App ID？
A: 访问 [飞书开放平台](https://open.feishu.cn/)，创建企业自建应用，在应用详情页获取

### Q: Gemini API Key从哪里获取？
A: 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)，创建API Key

### Q: 为什么图片无法显示？
A: 确保：1) 对文档有访问权限 2) Token未过期 3) 网络连接正常

### Q: AI生成失败怎么办？
A: 检查：1) Gemini API Key是否正确 2) 是否超出配额 3) 网络是否可访问Google服务

更多问题请查看 [配置指南.md](./配置指南.md) 的常见问题章节

## 🛠️ 开发路线图

- [x] MVP - 基础文章生成
- [x] V1.0 - 图片处理能力
- [x] V1.1 - 多轮对话精修 ⭐ 当前版本
- [ ] V1.2 - 导出为Word/PDF
- [ ] V1.3 - 创作模板库
- [ ] V2.0 - 团队协作功能

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE)

---

**让创作更简单，让AI成为你的写作伙伴！✨**


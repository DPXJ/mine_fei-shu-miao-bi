# 🤖 飞书文档AI助手小组件

基于React + TypeScript开发的飞书文档小组件，提供智能内容创作功能。

## ✨ 功能特性

- 📄 **智能文档读取** - 自动读取当前文档的文本和图片内容
- 🤖 **AI内容生成** - 基于千问VL模型生成高质量文章
- 🔄 **多轮对话优化** - 支持内容精修和迭代优化
- 📝 **一键插入** - 生成的内容直接插入到飞书文档
- 🎨 **美观界面** - 基于Ant Design的精美UI
- 🔧 **开发友好** - 支持开发模式和生产模式

## 🚀 快速开始

### 方法1: 使用脚本 (推荐)

```bash
# 1. 安装依赖
install.bat

# 2. 启动开发服务器
start.bat
```

### 方法2: 手动操作

```bash
# 1. 安装依赖
npm install

# 2. 启动后端服务 (新终端)
cd ../backend_py
python main.py

# 3. 启动小组件 (新终端)
cd ../feishu-widget
npm run dev
```

### 4. 访问应用

- 小组件地址: http://localhost:3001
- 后端API文档: http://localhost:8000/docs

## 🏗️ 技术架构

```
飞书文档
  ↓
【AI助手小组件】 (React + TypeScript)
  ↓ HTTP API
【FastAPI后端】 (Python)
  ↓
【千问VL AI】 (阿里云)
```

## 📁 项目结构

```
feishu-widget/
├── src/
│   ├── App.tsx              # 主组件
│   ├── services/
│   │   ├── api.ts           # 后端API调用
│   │   └── feishu.ts        # 飞书SDK封装
│   └── App.css              # 样式文件
├── public/
│   ├── index.html           # HTML模板
│   └── manifest.json        # 飞书应用配置
├── install.bat              # 依赖安装脚本
├── start.bat                # 启动脚本
├── package.json             # 项目配置
├── webpack.config.js        # 打包配置
└── README.md                # 说明文档
```

## 🔧 开发指南

### 环境要求

- Node.js 16+
- npm 或 yarn
- Python 3.8+ (后端)
- 飞书开发者账号 (生产部署)

### 核心依赖

```json
{
  "react": "^18.2.0",
  "typescript": "^5.3.0",
  "antd": "^5.12.0",
  "@lark-base-open/js-sdk": "^1.2.0",
  "@lark-base-open/ui": "^0.1.0"
}
```

### 开发模式 vs 生产模式

**开发模式** (本地测试):
- 使用模拟文档数据
- 内容显示在界面上，可手动复制
- 无需飞书开发者账号

**生产模式** (飞书环境):
- 读取真实文档内容
- 内容直接插入到飞书文档
- 需要配置飞书应用权限

## 🎯 核心功能

### 1. 文档内容读取

```typescript
// 读取当前文档的所有内容
const content = await readDocumentContent();
console.log('文本段落:', content.texts);
console.log('图片数量:', content.images.length);
```

### 2. AI内容生成

```typescript
// 调用后端AI生成接口
const result = await generateArticle({
  texts: docContent.texts.join('\n\n'),
  images: docContent.images,
  instruction: '请帮我润色这段内容'
});
```

### 3. 内容插入

```typescript
// 将生成的内容插入到文档末尾
await insertTextContent(result.content, 'end');
```

## 🔌 后端API集成

小组件复用现有的FastAPI后端:

- `POST /api/ai/create` - AI内容生成
- `POST /api/ai/refine` - 多轮对话优化
- `GET /api/ai/preview/{session_id}` - 获取预览

## 📱 飞书应用配置

### 1. 创建飞书应用

1. 登录 [飞书开发者后台](https://open.feishu.cn/app)
2. 创建新应用 → 选择 "文档小组件"
3. 配置权限:
   - ✅ `docx:read` - 读取文档内容
   - ✅ `docx:write` - 编辑文档内容

### 2. 配置回调地址

```
开发环境: http://localhost:3001
生产环境: https://your-domain.com
```

### 3. 应用信息

```json
{
  "name": "AI文档助手",
  "description": "智能内容创作,让你的文档更专业",
  "version": "1.0.0",
  "type": "doc_block",
  "permissions": ["docx:read", "docx:write"]
}
```

## 🧪 测试指南

### 1. 本地测试

```bash
# 启动服务
npm run dev

# 访问 http://localhost:3001
# 测试各项功能
```

### 2. 飞书环境测试

1. 将应用部署到服务器
2. 在飞书文档中插入小组件
3. 测试真实文档读取和内容插入

### 3. 功能测试清单

- [ ] 文档内容读取正常
- [ ] AI生成功能正常
- [ ] 多轮对话优化正常
- [ ] 内容插入到文档正常
- [ ] 错误处理完善
- [ ] UI界面美观

## 🚀 部署指南

### 1. 构建生产版本

```bash
npm run build
```

### 2. 部署到服务器

将 `dist/` 目录部署到Web服务器

### 3. 配置飞书应用

更新应用的回调地址为生产环境URL

### 4. 提交审核

在飞书开发者后台提交应用审核

## 🐛 故障排除

### 常见问题

**Q: 依赖安装失败**
```bash
# 使用国内镜像
npm install --registry=https://registry.npmmirror.com
```

**Q: 无法读取文档内容**
- 检查飞书应用权限配置
- 确认在飞书环境中运行

**Q: 内容插入失败**
- 检查用户是否有文档编辑权限
- 确认飞书SDK版本兼容性

**Q: 后端API调用失败**
- 确认后端服务已启动 (http://localhost:8000)
- 检查CORS配置

### 调试技巧

1. 打开浏览器开发者工具
2. 查看Console日志
3. 检查Network请求
4. 参考后端API文档

## 📞 技术支持

- 项目文档: 查看项目根目录的 `*.md` 文件
- 后端API: http://localhost:8000/docs
- 飞书开发文档: https://open.feishu.cn/

## 📄 许可证

MIT License

---

**🎉 开始你的飞书文档AI助手之旅！**
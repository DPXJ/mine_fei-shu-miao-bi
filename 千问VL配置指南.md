# 🎨 千问VL配置指南（支持图片理解）

## 📋 为什么选择千问VL？

- ✅ **支持图片理解**：能"看懂"图片内容
- ✅ **智能排版**：根据图片与文本关联性自动排版
- ✅ **国内直接可用**：无需VPN，速度快
- ✅ **免费额度**：新用户有免费额度可用
- ✅ **效果优秀**：中文理解能力强

---

## 🚀 第一步：获取千问API Key

### 1. 访问千问官网

打开浏览器，访问：**https://dashscope.console.aliyun.com/**

### 2. 注册/登录账号

**如果没有阿里云账号**：
- 点击"注册"
- 使用手机号注册即可
- 完成手机号验证

**如果有阿里云账号**：
- 直接登录

### 3. 开通DashScope服务

登录后：
1. 找到"灵积模型服务"（DashScope）
2. 点击"立即开通"
3. 阅读并同意服务协议
4. 开通成功（有免费额度）

### 4. 创建API Key

1. 在左侧菜单找到 **"API-KEY管理"**
2. 点击 **"创建新的API-KEY"**
3. 输入Key名称（例如：`飞书妙笔`）
4. 点击"确定"
5. **复制生成的API Key**（格式类似：`sk-xxxxxxxxxxxxxxxx`）

⚠️ **重要**：API Key只显示一次，请立即复制保存！

---

## 🔧 第二步：修改项目配置

### 方法一：直接修改代码文件（推荐）

1. **打开文件**：`backend_py/main.py`

2. **找到第24行**，将：
```python
os.environ["QWEN_API_KEY"] = "你的千问API_Key_替换这里"
```

修改为：
```python
os.environ["QWEN_API_KEY"] = "sk-你刚才复制的API_Key"
```

3. **保存文件**

### 方法二：告诉我你的API Key

如果你不想自己改代码，可以：
1. 复制你获取到的千问API Key
2. 告诉我：`我的千问API Key是：sk-xxxxx`
3. 我帮你修改配置

---

## ✅ 第三步：重启后端服务

### 停止当前后端

如果后端正在运行：
- 在运行后端的终端按 `Ctrl + C` 停止

### 启动后端

**方法一：使用命令行**
```bash
cd backend_py
python main.py
```

**方法二：双击bat文件**
- 双击 `启动后端修复版.bat`

### 验证启动成功

你应该看到类似输出：
```
INFO:     Will watch for changes in these directories: [...]
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**关键**：不应该有 `QWEN_API_KEY environment variable is not set` 错误

---

## 🎯 第四步：测试图片理解功能

### 1. 访问前端

打开浏览器，访问：http://localhost:3000

### 2. 登录飞书

点击"使用飞书登录"并授权

### 3. 选择包含图片的文档

在文档列表中，选择一个包含图片的飞书文档

### 4. 输入创作指令

在编辑器输入：
```
根据图片内容，创作一篇图文并茂的文章，合理安排图片位置
```

### 5. 点击"生成"

AI会：
- ✅ 分析每张图片的内容
- ✅ 理解图片与文本的关联
- ✅ 将图片插入到最合适的位置

### 6. 预览排版效果

生成后，点击右上角 **"预览排版"** 按钮，查看图文混排效果

---

## 🔍 验证配置是否成功

### 方法一：查看后端日志

后端启动后，当你点击生成时，应该看到：
```
Using AI Provider: qwen
Calling Qwen VL API... (timeout=60s, images=3)
Added image 1 to content
Added image 2 to content
Added image 3 to content
Qwen VL API response received successfully
```

如果看到 `QWEN_API_KEY environment variable is not set`，说明配置有问题。

### 方法二：查看生成效果

如果配置成功，AI生成的文章中会包含图片占位符，例如：
```markdown
# 文章标题

开头内容...

![产品外观图](image_1)

继续内容...
```

---

## ❓ 常见问题

### Q1: 找不到"API-KEY管理"菜单？

**A:** 确保已经开通了"DashScope"服务。开通后，左侧菜单会出现"API-KEY管理"选项。

### Q2: API Key创建后在哪里查看？

**A:** API Key只在创建时显示一次！如果忘记保存，需要重新创建一个新的。

### Q3: 提示"余额不足"怎么办？

**A:** 
- 新用户有免费额度
- 如果用完了，需要在阿里云账户中充值
- 千问VL价格很便宜，几块钱可以用很久

### Q4: 后端启动失败，显示编码错误？

**A:** 这是之前的`.env`文件导致的。现在所有配置都在`main.py`中，不需要`.env`文件了。

### Q5: 还是不支持图片理解？

**A:** 检查以下几点：
1. `main.py`第25行是否设置了 `os.environ["AI_PROVIDER"] = "qwen"`
2. 千问API Key是否正确填写（第24行）
3. 后端是否重启
4. 后端日志中是否显示 `Using AI Provider: qwen`

### Q6: 想切换回DeepSeek怎么办？

**A:** 修改 `main.py` 第25行：
```python
# 注释掉这行
# os.environ["AI_PROVIDER"] = "qwen"

# 取消注释这行
os.environ["AI_PROVIDER"] = "deepseek"
```

---

## 💡 使用建议

### 最佳实践

1. **创作指令要明确**：
   - ✅ "根据图片内容，创作一篇产品介绍，合理排版图片"
   - ❌ "写一篇文章"（太笼统）

2. **充分利用图片理解**：
   - 让AI分析图片内容
   - 根据图片与文本的关联性排版

3. **多轮对话优化**：
   - 生成后可以继续输入指令优化
   - 例如："把第二张图片移到开头"

### 示例对话

**用户**：根据这些图片和文字，创作一篇产品介绍，图片要放在最合适的位置

**AI（千问VL）**：
```markdown
# 产品介绍

我们的产品结合了优雅的设计和强大的功能...

![产品外观展示](image_1)

从图片可以看出，产品采用了简约的设计风格...

![功能演示图](image_2)

核心功能包括...
```

---

## 🎉 配置完成！

现在你可以：
- ✅ 体验AI图片理解功能
- ✅ 智能排版图文内容
- ✅ 创作高质量的图文文章

**有任何问题，随时告诉我！** 🚀


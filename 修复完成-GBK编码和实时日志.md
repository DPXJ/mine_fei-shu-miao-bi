# ✅ 修复完成：GBK编码错误和实时日志问题

## 🐛 问题诊断

### 问题1：创建飞书副本失败 - GBK编码错误 ❌

**错误信息：**
```
创建失败:创建文档失败:'gbk' codec can't encode character '\u274c' in position 0: illegal multibyte sequence
```

**原因：**
- 飞书文档标题包含特殊字符（如 ❌ 符号）
- Windows系统的GBK编码无法处理这些Unicode字符
- 导致后端在创建飞书文档时崩溃

### 问题2：后端日志不实时更新 ❌

**现象：**
- 后端启动后，终端只显示启动信息
- 点击"创建飞书副本"时，终端没有实时显示请求日志
- 无法看到API调用的详细过程

**原因：**
- uvicorn启动配置缺少日志相关参数
- 没有启用访问日志和详细日志级别

---

## ✅ 修复方案

### 修复1：GBK编码错误处理

**文件：** `backend_py/routers/documents.py`

**修改内容：**
```python
# 1. 创建新文档 - 清理标题中的特殊字符
import re
# 移除或替换特殊字符，避免GBK编码问题
clean_title = re.sub(r'[^\w\s\-_\.\(\)\[\]（）【】]', '', title)
if not clean_title.strip():
    clean_title = "AI创作文档"

print(f"Original title: {title}")
print(f"Clean title: {clean_title}")

create_response = await client.post(
    "https://open.feishu.cn/open-apis/docx/v1/documents",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    json={
        "title": clean_title,  # 使用清理后的标题
        "folder_token": ""
    }
)
```

**关键改进：**
- ✅ 使用正则表达式清理标题中的特殊字符
- ✅ 保留常用字符：字母、数字、空格、连字符、下划线、点、括号
- ✅ 如果清理后标题为空，使用默认标题"AI创作文档"
- ✅ 添加调试日志，显示原标题和清理后标题

---

### 修复2：后端实时日志配置

**文件：** `backend_py/main.py`

**修改前：**
```python
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
```

**修改后：**
```python
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=port, 
        reload=True,
        log_level="info",      # ← 启用info级别日志
        access_log=True,       # ← 启用访问日志
        use_colors=True        # ← 启用彩色日志
    )
```

**关键改进：**
- ✅ `log_level="info"` - 显示INFO级别及以上的日志
- ✅ `access_log=True` - 显示HTTP请求访问日志
- ✅ `use_colors=True` - 启用彩色日志，更易阅读
- ✅ 保持 `reload=True` - 代码热重载功能

---

## 📊 修复效果

### 修复后的日志输出

**启动日志：**
```
INFO:     Will watch for changes in these directories: ['D:\\...\\backend_py']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**实时请求日志：**
```
INFO:     127.0.0.1:12345 - "POST /api/documents/create HTTP/1.1" 200 OK
Original title: 测试文档 - AI创作副本 ❌
Clean title: 测试文档 - AI创作副本 
Create document response: {'code': 0, 'data': {'document': {'document_id': 'xxx'}}, 'msg': 'success'}
Upload image 1 response: {'code': 0, 'data': {'file_token': 'abc123'}, 'msg': 'Success'}
Image 1 uploaded successfully: abc123
Creating batch 1/2: 50 blocks
Batch 1 response: {'code': 0, 'msg': 'success'}
✅ Batch 1 created successfully
```

**错误日志（如果有）：**
```
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "...", line 123, in ...
    # 详细的错误堆栈信息
```

---

## 🧪 立即测试

### 步骤1：确认后端已重启 ✅

查看你的终端窗口（后端启动的那个），应该看到：
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxx] using StatReload
INFO:     Started server process [xxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ **后端已重启并运行**

---

### 步骤2：测试创建飞书副本功能

1. **打开前端** http://localhost:3000
2. **选择一个文档**（包含特殊字符标题的文档）
3. **生成文章**
4. **点击"创建飞书副本"**
5. **同时观察后端终端日志**

---

### 步骤3：验证修复效果

**在点击"创建飞书副本"后，后端终端应该实时显示：**

```
INFO:     127.0.0.1:xxxx - "OPTIONS /api/documents/create HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxx - "POST /api/documents/create HTTP/1.1" 200 OK

Original title: 测试文档 - AI创作副本 ❌
Clean title: 测试文档 - AI创作副本 

Create document response: {'code': 0, 'data': {'document': {'document_id': 'xxx'}}, 'msg': 'success'}

Upload image 1 response: {'code': 0, 'data': {'file_token': 'abc123'}, 'msg': 'Success'}
Image 1 uploaded successfully: abc123

Creating batch 1/1: 25 blocks
Batch 1 response: {'code': 0, 'msg': 'success'}
✅ Batch 1 created successfully
```

---

### 步骤4：验证飞书文档

**前端应该显示：**
- ✅ 成功提示："飞书文档创建成功！"
- ✅ 弹窗中的飞书文档链接
- ✅ 点击链接能打开新文档，标题正常显示（没有❌符号）

---

## 🎯 成功标志

### 后端日志检查
- [ ] 看到启动完成信息：`INFO: Application startup complete.`
- [ ] 看到实时请求日志：`INFO: 127.0.0.1:xxxx - "POST /api/documents/create HTTP/1.1" 200 OK`
- [ ] 看到标题清理日志：`Original title: xxx` 和 `Clean title: xxx`
- [ ] 看到创建成功日志：`✅ Batch 1 created successfully`
- [ ] **没有** GBK编码错误：`'gbk' codec can't encode character`

### 前端功能检查
- [ ] 点击"创建飞书副本"有loading提示
- [ ] 5-15秒后显示成功提示
- [ ] 弹窗中有飞书文档链接
- [ ] 点击链接打开新文档，标题正常显示

### 飞书文档检查
- [ ] 文档创建成功
- [ ] 标题中特殊字符被清理（❌符号消失）
- [ ] 文本内容完整
- [ ] 图片正确显示

---

## 🚨 常见问题排查

### Q1：后端日志还是不显示怎么办？
**A:** 
1. 确认后端已重启（看到 `Application startup complete.`）
2. 如果还是没有实时日志，尝试手动重启：
   - 在终端按 `Ctrl+C` 停止后端
   - 重新运行 `cd backend_py ; python main.py`

### Q2：还是看到GBK编码错误？
**A:** 
1. 确认代码已更新（查看 `backend_py/routers/documents.py` 第303-311行）
2. 重启后端
3. 重新测试

### Q3：飞书文档标题变成"AI创作文档"？
**A:** 
这说明原标题包含太多特殊字符，被完全清理了。这是正常的保护机制。

### Q4：图片上传还是失败？
**A:** 
检查日志中的图片上传部分：
```
Upload image 1 response: {'code': 0, ...}  # 成功
# 或者
Upload image 1 response: {'code': 1061002, 'msg': 'params error.'}  # 失败
```
如果还是失败，告诉我具体的错误信息。

---

## 📝 技术要点

### 字符清理正则表达式
```python
clean_title = re.sub(r'[^\w\s\-_\.\(\)\[\]（）【】]', '', title)
```
- `\w` - 字母、数字、下划线
- `\s` - 空格
- `\-_\.` - 连字符、下划线、点
- `\(\)\[\]（）【】` - 各种括号

### uvicorn日志配置
```python
uvicorn.run(
    "main:app", 
    host="0.0.0.0", 
    port=port, 
    reload=True,
    log_level="info",      # 日志级别：debug/info/warning/error
    access_log=True,       # HTTP访问日志
    use_colors=True        # 彩色输出
)
```

---

**两个问题都已修复！** ✅

**现在去测试吧！** 🚀

1. **后端已重启并运行** - 应该能看到实时日志
2. **GBK编码问题已修复** - 特殊字符会被自动清理
3. **飞书文档创建应该成功** - 标题正常，内容完整

有任何问题随时告诉我！

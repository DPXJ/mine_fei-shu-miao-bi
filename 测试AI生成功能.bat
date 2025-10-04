@echo off
chcp 65001 >nul
echo ========================================
echo 飞书妙笔 - 测试AI生成功能
echo ========================================

echo.
echo 🎯 已修复的问题：
echo ✓ 后端服务启动问题（.env文件缺失）
echo ✓ 文本内容显示问题
echo ✓ AI生成功能配置
echo.
echo 现在测试AI生成功能：
echo 1. 访问 http://localhost:3000
echo 2. 登录飞书账号
echo 3. 打开"测试"文档
echo 4. 在底部输入框中输入："帮我润色一下"
echo 5. 点击"生成"按钮
echo 6. 查看后端终端窗口的调试日志
echo 7. 检查浏览器Network标签页的API请求
echo.
echo 后端日志应该显示：
echo - AI Create request received: doc_id=..., blocks_count=X
echo - Gemini API Key configured: AIzaSyBKO6...
echo - Initializing Gemini model...
echo - Generated prompt length: XXXX
echo - Calling Gemini API...
echo - Gemini API response received
echo - Generated text length: XXXX
echo.
echo 前端Network标签页应该显示：
echo - POST请求到 http://localhost:8000/api/ai/create
echo - 状态码: 200 OK
echo - 响应包含 session_id 和 content
echo.
echo 预期结果：
echo - 生成的文章应该显示在右侧主要内容区域
echo - 支持多轮对话（再次输入指令进行精修）
echo - 文章内容应该基于文档内容进行AI创作
echo.
echo 🚀 现在应该能正常使用AI生成功能了！
echo.
pause

@echo off
chcp 65001 >nul
echo ========================================
echo 飞书妙笔 - 测试文档内容获取
echo ========================================

echo.
echo 🎯 已修复的问题：
echo ✓ .env文件编码问题已解决
echo ✓ 后端服务已启动
echo ✓ 按照飞书官方文档修复了API调用
echo.
echo 现在测试步骤：
echo 1. 访问 http://localhost:3000
echo 2. 登录飞书账号
echo 3. 打开"测试"文档
echo 4. 查看后端终端窗口的调试日志
echo 5. 检查浏览器控制台的输出
echo.
echo 后端日志应该显示：
echo - Fetching blocks for doc_id: RLMKdRrNqo9OtyxKkP2cFgtZnQg
echo - Blocks API response code: 0
echo - Found X blocks
echo - Block 0: type=1, id=...
echo - Text content structure: {...}
echo - Extracted text: '测试一下,我只是试一下...'
echo - Added text block: 测试一下,我只是试一下...
echo - Total content blocks created: X
echo.
echo 前端控制台应该显示：
echo - blocks: Array(X) 而不是 Array(0)
echo - Text blocks: [{...}]
echo.
echo 如果仍然显示 Array(0)，请提供：
echo 1. 后端终端窗口的完整日志
echo 2. 浏览器Network标签页的API响应
echo 3. 具体的错误信息
echo.
echo 🚀 现在应该能看到文档的文本内容了！
echo.
pause

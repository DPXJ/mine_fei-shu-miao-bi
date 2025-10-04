@echo off
chcp 65001 >nul
echo ========================================
echo 飞书妙笔 - 测试文本提取修复
echo ========================================

echo.
echo 已修复的问题：
echo ✓ 扩展了block_type支持范围（1-10）
echo ✓ 尝试多种文本字段（text, paragraph, content）
echo ✓ 尝试多种元素路径（elements, children, content）
echo ✓ 改进了文本提取函数
echo ✓ 添加了详细的调试日志
echo.
echo 测试步骤：
echo 1. 访问 http://localhost:3000
echo 2. 登录飞书账号
echo 3. 打开"测试"文档
echo 4. 查看浏览器控制台和文档内容预览区域
echo 5. 查看后端终端窗口的详细日志
echo.
echo 后端日志应该显示：
echo - Total blocks found: X
echo - Raw blocks sample: [...]
echo - Block type: X, block_id: ...
echo - Full block: {...}
echo - Text content: {...}
echo - Elements: [...]
echo - Extracted text: '...'
echo.
echo 如果仍然没有文本内容，请提供后端日志的完整输出
echo.
pause

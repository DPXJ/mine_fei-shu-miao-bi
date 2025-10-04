@echo off
chcp 65001 >nul
echo ========================================
echo 飞书妙笔 - 最终文本修复测试
echo ========================================

echo.
echo 🎯 重大修复：使用飞书纯文本API
echo.
echo 修复内容：
echo ✓ 使用飞书官方纯文本API: /doc/v2/{docToken}/raw_content
echo ✓ 直接获取文档的纯文本内容，无需解析复杂blocks
echo ✓ 保留图片获取功能
echo ✓ 添加回退机制（如果纯文本API失败）
echo ✓ 详细的调试日志
echo.
echo 测试步骤：
echo 1. 访问 http://localhost:3000
echo 2. 登录飞书账号
echo 3. 打开"测试"文档
echo 4. 查看右侧"文档内容预览"区域
echo 5. 检查浏览器控制台日志
echo 6. 查看后端终端窗口的详细日志
echo.
echo 后端日志应该显示：
echo - Fetching raw content for doc_id: ...
echo - Raw content response: {...}
echo - Raw text content: '测试一下,我只是试一下...'
echo - Added text block with X characters
echo.
echo 前端控制台应该显示：
echo - Document content loaded: {doc_id: '...', title: '测试', blocks: Array(1)}
echo - Blocks: [{block_id: 'text_...', block_type: 'text', text: '测试一下...'}]
echo - Text blocks: [{block_id: 'text_...', block_type: 'text', text: '测试一下...'}]
echo.
echo 🚀 现在应该能看到文档的文本内容了！
echo.
pause

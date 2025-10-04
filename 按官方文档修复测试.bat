@echo off
chcp 65001 >nul
echo ========================================
echo 飞书妙笔 - 按官方文档修复测试
echo ========================================

echo.
echo 🎯 重大修复：按照飞书官方文档修复
echo.
echo 修复内容：
echo ✓ 使用正确的blocks API调用方式
echo ✓ 添加了document_revision_id=-1参数
echo ✓ 添加了user_id_type=open_id参数
echo ✓ 改进了错误处理和调试日志
echo ✓ 按照官方文档的block_type=1处理文本块
echo.
echo 参考文档：
echo https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document/list
echo.
echo 测试步骤：
echo 1. 访问 http://localhost:3000
echo 2. 登录飞书账号
echo 3. 打开"测试"文档
echo 4. 查看后端终端窗口的详细日志
echo 5. 检查浏览器控制台的blocks数组
echo.
echo 后端日志应该显示：
echo - Fetching blocks for doc_id: ...
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
echo 🚀 现在应该能看到文档的文本内容了！
echo.
pause

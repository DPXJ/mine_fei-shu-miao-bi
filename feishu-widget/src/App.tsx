import React, { useState, useEffect } from 'react';
import { Card, Input, Button, Space, message, Typography, Spin, Tag, Alert } from 'antd';
import { ThunderboltOutlined, FileTextOutlined, PictureOutlined, PlusOutlined } from '@ant-design/icons';
import { generateArticle } from './services/api';
import './App.css';

const { TextArea } = Input;
const { Title, Text, Paragraph } = Typography;

interface DocumentContent {
  texts: string[];
  images: string[];
}

const App: React.FC = () => {
  const [docContent, setDocContent] = useState<DocumentContent>({ texts: [], images: [] });
  const [instruction, setInstruction] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingDoc, setLoadingDoc] = useState(true);
  const [generatedContent, setGeneratedContent] = useState('');
  const [sessionId, setSessionId] = useState('');

  // 模拟文档内容加载
  useEffect(() => {
    const loadDocContent = async () => {
      setLoadingDoc(true);
      try {
        // 开发模式：使用模拟数据
        const mockTexts = [
          '# 测试文档标题',
          '这是一段测试内容，用于演示AI文档助手的功能。',
          'GitHub配机子,还有Couplate WeFly、腾讯库和阿里云。',
          '## 二级标题',
          '这里是一些示例文本，展示多级标题的效果。'
        ];
        const mockImages = ['mock_image_token_1', 'mock_image_token_2'];
        
        setDocContent({ 
          texts: mockTexts, 
          images: mockImages 
        });
        message.success('已加载模拟文档内容');
      } catch (error) {
        console.error('加载文档失败:', error);
        message.error('读取文档失败,请刷新重试');
      } finally {
        setLoadingDoc(false);
      }
    };
    
    loadDocContent();
  }, []);

  // AI生成
  const handleGenerate = async () => {
    if (!instruction.trim()) {
      message.warning('请输入AI指令');
      return;
    }

    if (docContent.texts.length === 0) {
      message.warning('文档内容为空,无法生成');
      return;
    }

    setLoading(true);
    setGeneratedContent('');
    
    try {
      // 调用后端API
      const result = await generateArticle({
        texts: docContent.texts.join('\n\n'),
        images: docContent.images,
        instruction: instruction
      });

      setGeneratedContent(result.content);
      setSessionId(result.session_id);
      message.success('内容已生成!');
      
    } catch (error: any) {
      console.error('生成失败:', error);
      message.error(error.message || '生成失败,请重试');
    } finally {
      setLoading(false);
    }
  };

  // 多轮对话优化
  const handleRefine = async () => {
    if (!sessionId) {
      message.warning('请先生成内容');
      return;
    }

    if (!instruction.trim()) {
      message.warning('请输入优化指令');
      return;
    }

    setLoading(true);
    
    try {
      // 调用后端refine API
      const response = await fetch('http://localhost:8000/api/ai/refine', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          instruction: instruction
        })
      });

      if (!response.ok) {
        throw new Error('优化请求失败');
      }

      const result = await response.json();
      setGeneratedContent(result.content);
      message.success('内容已优化!');
      
    } catch (error: any) {
      console.error('优化失败:', error);
      message.error('优化失败: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  // 预设指令
  const presetInstructions = [
    { label: '润色', value: '请帮我润色这段内容,使其更加流畅自然' },
    { label: '专业化', value: '请将内容改写得更专业、正式' },
    { label: '活泼化', value: '请将内容改写得更活泼、生动有趣' },
    { label: '简洁化', value: '请将内容精简,保留核心要点' }
  ];

  if (loadingDoc) {
    return (
      <div style={{ padding: 40, textAlign: 'center' }}>
        <Spin size="large" tip="加载文档内容中..." />
      </div>
    );
  }

  return (
    <div style={{ padding: 20, maxWidth: 800, margin: '0 auto' }}>
      <Card>
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          {/* 标题 */}
          <div style={{ textAlign: 'center' }}>
            <Title level={3}>
              <ThunderboltOutlined /> 🤖 AI文档助手
            </Title>
            <Text type="secondary">智能理解文档内容,一键生成高质量文章</Text>
            
            {/* 环境提示 */}
            <Alert
              message="开发模式"
              description="正在使用模拟数据，实际部署后会读取真实文档内容"
              type="info"
              showIcon
              style={{ marginTop: 12 }}
            />
          </div>

          {/* 文档预览 */}
          <Card size="small" title="📄 当前文档">
            <Space>
              <Tag icon={<FileTextOutlined />} color="blue">
                {docContent.texts.length} 段文本
              </Tag>
              <Tag icon={<PictureOutlined />} color="green">
                {docContent.images.length} 张图片
              </Tag>
            </Space>
            {docContent.texts.length > 0 && (
              <Paragraph 
                ellipsis={{ rows: 3, expandable: true }} 
                style={{ marginTop: 12, marginBottom: 0 }}
              >
                {docContent.texts.join('\n\n')}
              </Paragraph>
            )}
          </Card>

          {/* AI指令输入 */}
          <div>
            <Text strong style={{ display: 'block', marginBottom: 8 }}>
              ✨ AI指令
            </Text>
            <TextArea
              placeholder="请输入你的需求,例如: 润色、专业化、活泼化..."
              value={instruction}
              onChange={(e) => setInstruction(e.target.value)}
              rows={3}
              showCount
              maxLength={500}
            />
          </div>

          {/* 预设按钮 */}
          <div>
            <Text type="secondary" style={{ display: 'block', marginBottom: 8 }}>
              快捷指令:
            </Text>
            <Space wrap>
              {presetInstructions.map(preset => (
                <Button
                  key={preset.label}
                  size="small"
                  onClick={() => setInstruction(preset.value)}
                >
                  {preset.label}
                </Button>
              ))}
            </Space>
          </div>

          {/* 操作按钮组 */}
          <Space direction="vertical" style={{ width: '100%' }}>
            <Button 
              type="primary" 
              onClick={handleGenerate}
              loading={loading}
              block
              size="large"
              icon={<ThunderboltOutlined />}
            >
              {loading ? '生成中...' : '✨ 生成内容'}
            </Button>
            
            {generatedContent && (
              <Space style={{ width: '100%', justifyContent: 'space-between' }}>
                <Button 
                  onClick={() => {
                    navigator.clipboard.writeText(generatedContent);
                    message.success('内容已复制到剪贴板');
                  }}
                  icon={<PlusOutlined />}
                  disabled={loading}
                >
                  📋 复制内容
                </Button>
                <Button 
                  onClick={handleRefine}
                  disabled={loading || !sessionId}
                  loading={loading}
                >
                  🔄 优化内容
                </Button>
              </Space>
            )}
          </Space>

          {/* 生成结果 */}
          {generatedContent && (
            <Card 
              size="small" 
              title="✅ 生成结果" 
              extra={
                <Button 
                  type="link" 
                  size="small"
                  onClick={() => {
                    navigator.clipboard.writeText(generatedContent);
                    message.success('已复制到剪贴板');
                  }}
                >
                  复制
                </Button>
              }
            >
              <div style={{ 
                maxHeight: 400, 
                overflow: 'auto',
                whiteSpace: 'pre-wrap',
                wordBreak: 'break-word'
              }}>
                {generatedContent}
              </div>
            </Card>
          )}
        </Space>
      </Card>

      {/* 提示 */}
      <div style={{ textAlign: 'center', marginTop: 20 }}>
        <Text type="secondary" style={{ fontSize: 12 }}>
          💡 提示: 开发模式下使用模拟数据，部署后支持真实文档操作
        </Text>
      </div>
    </div>
  );
};

export default App;
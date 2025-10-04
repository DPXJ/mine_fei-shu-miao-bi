"""
AI提供商通用接口
支持: Gemini (多模态), DeepSeek (文本), 千问VL (多模态)
"""
import os
import httpx
import base64
from typing import Optional, List, Dict, Any, Union
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

# 尝试导入Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class AIProvider:
    """AI提供商基类"""
    
    @staticmethod
    def create(provider: str = None):
        """工厂方法创建AI提供商实例"""
        if provider is None:
            provider = os.getenv("AI_PROVIDER", "gemini")
        
        if provider.lower() == "gemini":
            return GeminiProvider()
        elif provider.lower() == "deepseek":
            return DeepSeekProvider()
        elif provider.lower() == "qwen":
            return QwenVLProvider()
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")
    
    def generate(self, prompt: str, images: List[Dict] = None, timeout: int = 30) -> str:
        """
        生成文本内容
        
        Args:
            prompt: 文本提示
            images: 图片列表，格式：[{"mime_type": "image/jpeg", "data": "base64_string"}, ...]
            timeout: 超时时间（秒）
        """
        raise NotImplementedError
    
    def supports_multimodal(self) -> bool:
        """是否支持多模态（图片理解）"""
        return False


class GeminiProvider(AIProvider):
    """Google Gemini提供商 - 支持多模态（图片理解）"""
    
    def __init__(self):
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai not installed")
        
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-pro")
    
    def supports_multimodal(self) -> bool:
        return True
    
    def generate(self, prompt: str, images: List[Dict] = None, timeout: int = 30) -> str:
        """调用Gemini API生成内容 - 支持图片"""
        print(f"Calling Gemini API... (timeout={timeout}s, images={len(images) if images else 0})")
        
        def call_api():
            # 构建内容列表
            contents = [prompt]
            
            # 如果有图片，添加到内容中
            if images:
                for img_data in images:
                    # Gemini支持直接传入PIL Image或base64
                    import io
                    from PIL import Image
                    
                    # 解码base64图片
                    img_bytes = base64.b64decode(img_data["data"])
                    img = Image.open(io.BytesIO(img_bytes))
                    contents.append(img)
            
            response = self.model.generate_content(
                contents,
                generation_config=genai.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=4096,
                )
            )
            return response.text
        
        # 使用线程池和超时
        with ThreadPoolExecutor() as executor:
            future = executor.submit(call_api)
            try:
                result = future.result(timeout=timeout)
                print("Gemini API response received successfully")
                return result
            except FuturesTimeoutError:
                print(f"Gemini API call timed out after {timeout} seconds")
                raise TimeoutError(f"Gemini API请求超时（{timeout}秒）- 可能是网络问题或地区限制。建议：1) 开启VPN 2) 切换到DeepSeek")
            except Exception as e:
                print(f"Gemini API call failed: {e}")
                raise


class DeepSeekProvider(AIProvider):
    """DeepSeek提供商（国内访问更稳定，仅支持文本）"""
    
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
        
        self.base_url = "https://api.deepseek.com"
        self.model = "deepseek-chat"
    
    def supports_multimodal(self) -> bool:
        return False
    
    def generate(self, prompt: str, images: List[Dict] = None, timeout: int = 30) -> str:
        """调用DeepSeek API生成内容（仅文本）"""
        if images:
            print("⚠️ Warning: DeepSeek does not support image understanding. Images will be ignored.")
        
        print(f"Calling DeepSeek API... (timeout={timeout}s)")
        
        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 4096
        }
        
        try:
            with httpx.Client(timeout=timeout) as client:
                response = client.post(url, json=data, headers=headers)
                response.raise_for_status()
                result = response.json()
                
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"]
                    print("DeepSeek API response received successfully")
                    return content
                else:
                    raise Exception("DeepSeek API returned invalid response")
        
        except httpx.TimeoutException:
            print(f"DeepSeek API call timed out after {timeout} seconds")
            raise TimeoutError(f"DeepSeek API请求超时（{timeout}秒）")
        except Exception as e:
            print(f"DeepSeek API call failed: {e}")
            raise


class QwenVLProvider(AIProvider):
    """阿里千问VL提供商 - 支持多模态（图片理解），国内可用"""
    
    def __init__(self):
        self.api_key = os.getenv("QWEN_API_KEY")
        if not self.api_key:
            raise ValueError("QWEN_API_KEY environment variable is not set")
        
        self.base_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
        self.model = "qwen-vl-plus"
    
    def supports_multimodal(self) -> bool:
        return True
    
    def generate(self, prompt: str, images: List[Dict] = None, timeout: int = 30) -> str:
        """调用千问VL API生成内容 - 支持图片理解"""
        print(f"Calling Qwen VL API... (timeout={timeout}s, images={len(images) if images else 0})")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 构建消息内容
        content = []
        
        # 添加图片（如果有）
        if images:
            for idx, img_data in enumerate(images, 1):
                content.append({
                    "image": f"data:{img_data['mime_type']};base64,{img_data['data']}"
                })
                print(f"Added image {idx} to content")
        
        # 添加文本提示
        content.append({"text": prompt})
        
        data = {
            "model": self.model,
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            },
            "parameters": {
                "max_tokens": 4096
            }
        }
        
        try:
            with httpx.Client(timeout=timeout) as client:
                response = client.post(self.base_url, json=data, headers=headers)
                response.raise_for_status()
                result = response.json()
                
                if "output" in result and "choices" in result["output"]:
                    content_text = result["output"]["choices"][0]["message"]["content"]
                    # 千问VL返回的content可能是列表
                    if isinstance(content_text, list):
                        content_text = "".join([item.get("text", "") for item in content_text if item.get("text")])
                    print("Qwen VL API response received successfully")
                    return content_text
                else:
                    raise Exception("Qwen VL API returned invalid response")
        
        except httpx.TimeoutException:
            print(f"Qwen VL API call timed out after {timeout} seconds")
            raise TimeoutError(f"千问VL API请求超时（{timeout}秒）")
        except Exception as e:
            print(f"Qwen VL API call failed: {e}")
            raise


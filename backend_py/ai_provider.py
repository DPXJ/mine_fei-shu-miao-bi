"""
AI提供商通用接口
支持: Gemini, DeepSeek
"""
import os
import httpx
from typing import Optional
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
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")
    
    def generate(self, prompt: str, timeout: int = 30) -> str:
        """生成文本内容"""
        raise NotImplementedError


class GeminiProvider(AIProvider):
    """Google Gemini提供商"""
    
    def __init__(self):
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai not installed")
        
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-pro")
    
    def generate(self, prompt: str, timeout: int = 30) -> str:
        """调用Gemini API生成内容"""
        print(f"Calling Gemini API... (timeout={timeout}s)")
        
        def call_api():
            response = self.model.generate_content(
                [prompt],
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
    """DeepSeek提供商（国内访问更稳定）"""
    
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
        
        self.base_url = "https://api.deepseek.com"
        self.model = "deepseek-chat"
    
    def generate(self, prompt: str, timeout: int = 30) -> str:
        """调用DeepSeek API生成内容"""
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


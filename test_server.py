#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试HTTP服务器是否正常工作
"""

import urllib.request
import urllib.error

def test_server():
    try:
        # 测试simple.html文件
        response = urllib.request.urlopen('http://localhost:3001/simple.html')
        if response.status == 200:
            print("✅ 服务器正常工作！")
            print(f"✅ simple.html 文件可以访问")
            print(f"✅ HTTP状态码: {response.status}")
            print(f"✅ 内容长度: {len(response.read())} 字节")
            return True
        else:
            print(f"❌ HTTP状态码错误: {response.status}")
            return False
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP错误: {e.code} - {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"❌ URL错误: {e.reason}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

if __name__ == "__main__":
    print("🔍 测试HTTP服务器...")
    test_server()

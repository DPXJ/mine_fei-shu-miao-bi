#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的HTTP服务器，用于测试feishu-widget小组件
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

# 设置控制台编码
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

# 设置端口
PORT = 3001

# 切换到feishu-widget/public目录
widget_dir = Path(__file__).parent / "feishu-widget" / "public"
if widget_dir.exists():
    os.chdir(widget_dir)
    print(f"✅ 切换到目录: {widget_dir}")
else:
    # 如果public目录不存在，尝试feishu-widget目录
    widget_dir = Path(__file__).parent / "feishu-widget"
    if widget_dir.exists():
        os.chdir(widget_dir)
        print(f"✅ 切换到目录: {widget_dir}")
    else:
        print(f"❌ 目录不存在: {widget_dir}")
        sys.exit(1)

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 添加CORS头，允许跨域访问
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        # 如果访问根路径，重定向到simple.html
        if self.path == '/':
            self.path = '/simple.html'
        return super().do_GET()

if __name__ == "__main__":
    print(f"🚀 启动飞书小组件测试服务器...")
    print(f"📍 服务地址: http://localhost:{PORT}")
    print(f"📁 服务目录: {os.getcwd()}")
    print(f"🌐 访问地址: http://localhost:{PORT}/simple.html")
    print("💡 按 Ctrl+C 停止服务器")
    print("-" * 50)

    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✅ 服务器已停止")
    except OSError as e:
        if e.errno == 10048:  # 端口被占用
            print(f"❌ 端口 {PORT} 被占用，请检查是否有其他服务在使用此端口")
        else:
            print(f"❌ 启动失败: {e}")
    except Exception as e:
        print(f"❌ 未知错误: {e}")

#!/usr/bin/env python3
"""皮肤照片服务：在 127.0.0.1:8899 提供 dsh-gui_edge 仓库目录的静态文件,
   供皮肤 CSS 用 http://127.0.0.1:8899/skin_figures/Solar_Halo_Painting.jpeg 引用。
   由 launchd (com.zezhong.dsh-skin-server) 托管, 开机自启。"""
import http.server
import socketserver
import sys
import os

# 根目录 = 显式参数, 默认取脚本所在目录的上级(仓库根)
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(ROOT)


class Handler(http.server.SimpleHTTPRequestHandler):
    directory = ROOT  # 不依赖进程 cwd

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


socketserver.TCPServer.allow_reuse_address = True
with socketserver.ThreadingTCPServer(("127.0.0.1", 8899), Handler) as httpd:
    httpd.serve_forever()

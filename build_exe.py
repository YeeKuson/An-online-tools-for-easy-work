"""
打包脚本 - 将工具集合网站打包为Windows可执行文件
"""

import os
import sys
from src.main import app

def create_app():
    """创建Flask应用实例"""
    return app

if __name__ == '__main__':
    # 确保上传和下载目录存在
    os.makedirs(os.path.join(os.path.dirname(__file__), 'src', 'static', 'uploads'), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'src', 'static', 'downloads'), exist_ok=True)
    
    # 启动应用
    app = create_app()
    app.run(host='0.0.0.0', port=5000)

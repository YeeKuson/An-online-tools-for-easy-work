"""
工具集合网站扩展指南

本文档提供了如何向工具集合网站添加新功能模块的指南。
"""

# 添加新工具模块的步骤

## 1. 创建模块目录结构

在 `src/routes/` 目录下为新工具创建一个新的目录，例如：

```
mkdir -p src/routes/new_tool_name
```

## 2. 创建模块初始化文件

在新创建的目录中创建 `__init__.py` 文件，定义蓝图：

```python
from flask import Blueprint

new_tool_bp = Blueprint('new_tool_name', __name__, url_prefix='/api/new-tool-name')

from src.routes.new_tool_name.routes import *
```

## 3. 实现API路由

在新创建的目录中创建 `routes.py` 文件，实现API功能：

```python
import os
import uuid
from flask import request, jsonify
from werkzeug.utils import secure_filename

from src.routes.new_tool_name import new_tool_bp

# 配置上传和下载路径
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'uploads')
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'downloads')

# 确保目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'xxx', 'yyy'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@new_tool_bp.route('/process', methods=['POST'])
def process_file():
    """
    处理文件的API
    
    请求参数:
    - file: 上传的文件
    - param1: 参数1
    - param2: 参数2
    
    返回:
    - 成功: {"success": true, "download_url": "下载链接"}
    - 失败: {"success": false, "error": "错误信息"}
    """
    # 实现处理逻辑
    pass
```

## 4. 在主程序中注册蓝图

在 `src/main.py` 文件中导入并注册新的蓝图：

```python
from src.routes.new_tool_name import new_tool_bp

# 注册蓝图
app.register_blueprint(new_tool_bp)
```

## 5. 创建前端页面

在 `src/templates/tools/` 目录下创建新工具的前端页面：

```
touch src/templates/tools/new-tool-name.html
```

使用现有工具页面作为模板，修改为新工具的功能。

## 6. 在首页添加入口

在 `src/templates/index.html` 文件中的卡片列表中添加新工具的入口：

```html
<div class="col">
    <div class="card h-100">
        <div class="card-body">
            <h5 class="card-title">新工具名称</h5>
            <p class="card-text">新工具的简短描述。</p>
            <a href="/tool/new-tool-name" class="btn btn-primary">使用工具</a>
        </div>
    </div>
</div>
```

## 7. 安装必要的依赖

如果新工具需要额外的Python库，请安装并更新requirements.txt：

```
pip install new_library
pip freeze > requirements.txt
```

## 8. 测试新功能

确保新功能在本地正常工作，然后部署到生产环境。

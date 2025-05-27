import os
import sys
from flask import Flask, render_template, send_from_directory

# 获取当前文件所在目录的绝对路径
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

# 创建Flask应用
app = Flask(__name__)

# 动态检测并设置模板和静态文件目录
if os.path.exists(os.path.join(CURRENT_DIR, 'src', 'templates')):
    # 如果main.py在项目根目录
    app.template_folder = os.path.join(CURRENT_DIR, 'src', 'templates')
    app.static_folder = os.path.join(CURRENT_DIR, 'src', 'static')
    UPLOAD_DIR = os.path.join(CURRENT_DIR, 'src', 'static', 'uploads')
    DOWNLOAD_DIR = os.path.join(CURRENT_DIR, 'src', 'static', 'downloads')
    ROUTES_DIR = os.path.join(CURRENT_DIR, 'src', 'routes')
elif os.path.exists(os.path.join(CURRENT_DIR, 'templates')):
    # 如果main.py在src目录
    app.template_folder = os.path.join(CURRENT_DIR, 'templates')
    app.static_folder = os.path.join(CURRENT_DIR, 'static')
    UPLOAD_DIR = os.path.join(CURRENT_DIR, 'static', 'uploads')
    DOWNLOAD_DIR = os.path.join(CURRENT_DIR, 'static', 'downloads')
    ROUTES_DIR = os.path.join(CURRENT_DIR, 'routes')
else:
    # 如果在web_tools_collection目录下
    app.template_folder = os.path.join(CURRENT_DIR, 'web_tools_collection', 'src', 'templates')
    app.static_folder = os.path.join(CURRENT_DIR, 'web_tools_collection', 'src', 'static')
    UPLOAD_DIR = os.path.join(CURRENT_DIR, 'web_tools_collection', 'src', 'static', 'uploads')
    DOWNLOAD_DIR = os.path.join(CURRENT_DIR, 'web_tools_collection', 'src', 'static', 'downloads')
    ROUTES_DIR = os.path.join(CURRENT_DIR, 'web_tools_collection', 'src', 'routes')

# 配置上传文件大小限制
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

# 确保上传和下载目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# 将路径添加到Python路径中，确保可以导入模块
if ROUTES_DIR not in sys.path:
    sys.path.insert(0, os.path.dirname(ROUTES_DIR))

# 导入并注册蓝图
try:
    from src.routes.pdf_to_word import pdf_to_word_bp
    from src.routes.word_to_pdf import word_to_pdf_bp
    from src.routes.pdf_to_image import pdf_to_image_bp
    from src.routes.image_concat import image_concat_bp
    from src.routes.image_resize import image_resize_bp
    from src.routes.pdf_to_ppt import pdf_to_ppt_bp
except ImportError:
    try:
        from routes.pdf_to_word import pdf_to_word_bp
        from routes.word_to_pdf import word_to_pdf_bp
        from routes.pdf_to_image import pdf_to_image_bp
        from routes.image_concat import image_concat_bp
        from routes.image_resize import image_resize_bp
        from routes.pdf_to_ppt import pdf_to_ppt_bp
    except ImportError:
        from web_tools_collection.src.routes.pdf_to_word import pdf_to_word_bp
        from web_tools_collection.src.routes.word_to_pdf import word_to_pdf_bp
        from web_tools_collection.src.routes.pdf_to_image import pdf_to_image_bp
        from web_tools_collection.src.routes.image_concat import image_concat_bp
        from web_tools_collection.src.routes.image_resize import image_resize_bp
        from web_tools_collection.src.routes.pdf_to_ppt import pdf_to_ppt_bp

app.register_blueprint(pdf_to_word_bp)
app.register_blueprint(word_to_pdf_bp)
app.register_blueprint(pdf_to_image_bp)
app.register_blueprint(image_concat_bp)
app.register_blueprint(image_resize_bp)
app.register_blueprint(pdf_to_ppt_bp)

# 主页路由
@app.route('/')
def index():
    return render_template('index.html')

# 工具页面路由
@app.route('/tool/<tool_name>')
def tool_page(tool_name):
    if tool_name in ['pdf-to-word', 'word-to-pdf', 'pdf-to-image', 'image-concat', 'image-resize', 'pdf-to-ppt']:
        return render_template(f'tools/{tool_name}.html')
    else:
        return render_template('404.html'), 404

# 静态文件路由
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# 下载文件路由
@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_DIR, filename)

if __name__ == '__main__':
    print("="*50)
    print("工具集合网站服务器启动中...")
    print(f"模板目录: {app.template_folder}")
    print(f"静态文件目录: {app.static_folder}")
    print(f"上传目录: {UPLOAD_DIR}")
    print(f"下载目录: {DOWNLOAD_DIR}")
    print("="*50)
    print("请在浏览器中访问: http://localhost:5000")
    print("="*50)
    
    # 启动应用
    app.run(host='0.0.0.0', port=5000, debug=True)

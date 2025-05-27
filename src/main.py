import os
from flask import Flask, render_template, send_from_directory
from src.routes.pdf_to_word import pdf_to_word_bp
from src.routes.word_to_pdf import word_to_pdf_bp
from src.routes.pdf_to_image import pdf_to_image_bp
from src.routes.image_concat import image_concat_bp
from src.routes.image_resize import image_resize_bp

# 创建Flask应用
app = Flask(__name__)

# 配置上传文件大小限制
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

# 注册蓝图
app.register_blueprint(pdf_to_word_bp)
app.register_blueprint(word_to_pdf_bp)
app.register_blueprint(pdf_to_image_bp)
app.register_blueprint(image_concat_bp)
app.register_blueprint(image_resize_bp)

# 主页路由
@app.route('/')
def index():
    return render_template('index.html')

# 工具页面路由
@app.route('/tool/<tool_name>')
def tool_page(tool_name):
    if tool_name in ['pdf-to-word', 'word-to-pdf', 'pdf-to-image', 'image-concat', 'image-resize']:
        return render_template(f'tools/{tool_name}.html')
    else:
        return render_template('404.html'), 404

# 静态文件路由
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# 下载文件路由
@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'downloads'), filename)

if __name__ == '__main__':
    # 确保上传和下载目录存在
    os.makedirs(os.path.join(app.root_path, 'static', 'uploads'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'static', 'downloads'), exist_ok=True)
    
    # 启动应用
    app.run(host='0.0.0.0', port=5000, debug=True)

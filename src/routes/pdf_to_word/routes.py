import os
import uuid
from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
from pdf2docx import Converter

from src.routes.pdf_to_word import pdf_to_word_bp

# 配置上传和下载路径
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'uploads')
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'downloads')

# 确保目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@pdf_to_word_bp.route('/convert', methods=['POST'])
def convert_pdf_to_word():
    """
    将PDF文件转换为Word文档
    
    请求参数:
    - file: PDF文件
    
    返回:
    - 成功: {"success": true, "download_url": "下载链接"}
    - 失败: {"success": false, "error": "错误信息"}
    """
    # 检查是否有文件上传
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': '没有上传文件'}), 400
    
    file = request.files['file']
    
    # 检查文件名是否为空
    if file.filename == '':
        return jsonify({'success': False, 'error': '未选择文件'}), 400
    
    # 检查文件类型
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': '不支持的文件类型，仅支持PDF文件'}), 400
    
    try:
        # 生成安全的文件名并保存上传的文件
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())
        pdf_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_{filename}")
        file.save(pdf_path)
        
        # 生成输出文件路径
        output_filename = f"{os.path.splitext(filename)[0]}.docx"
        output_path = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}_{output_filename}")
        
        # 执行PDF到Word的转换
        cv = Converter(pdf_path)
        cv.convert(output_path)
        cv.close()
        
        # 生成下载URL
        download_url = f"/static/downloads/{unique_id}_{output_filename}"
        
        # 删除上传的PDF文件（可选）
        # os.remove(pdf_path)
        
        return jsonify({
            'success': True, 
            'download_url': download_url,
            'filename': output_filename
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'转换过程中出错: {str(e)}'}), 500

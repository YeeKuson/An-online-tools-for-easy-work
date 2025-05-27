import os
import uuid
from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
import subprocess
import tempfile
from docx2pdf import convert

from src.routes.word_to_pdf import word_to_pdf_bp

# 配置上传和下载路径
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'uploads')
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'downloads')

# 确保目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'docx', 'doc'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@word_to_pdf_bp.route('/convert', methods=['POST'])
def convert_word_to_pdf():
    """
    将Word文档转换为PDF文件
    
    请求参数:
    - file: Word文件 (.docx 或 .doc)
    
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
        return jsonify({'success': False, 'error': '不支持的文件类型，仅支持Word文档 (.docx, .doc)'}), 400
    
    try:
        # 生成安全的文件名并保存上传的文件
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())
        word_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_{filename}")
        file.save(word_path)
        
        # 生成输出文件路径
        output_filename = f"{os.path.splitext(filename)[0]}.pdf"
        output_path = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}_{output_filename}")
        
        # 使用LibreOffice进行转换 (备选方案)
        try:
            # 尝试使用docx2pdf库进行转换
            convert(word_path, output_path)
        except Exception as e:
            # 如果docx2pdf失败，尝试使用LibreOffice
            subprocess.run([
                'libreoffice', '--headless', '--convert-to', 'pdf',
                '--outdir', DOWNLOAD_FOLDER, word_path
            ], check=True)
            
            # 重命名输出文件以匹配预期的命名格式
            temp_output = os.path.join(DOWNLOAD_FOLDER, f"{os.path.splitext(os.path.basename(word_path))[0]}.pdf")
            os.rename(temp_output, output_path)
        
        # 生成下载URL
        download_url = f"/static/downloads/{unique_id}_{output_filename}"
        
        # 删除上传的Word文件（可选）
        # os.remove(word_path)
        
        return jsonify({
            'success': True, 
            'download_url': download_url,
            'filename': output_filename
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'转换过程中出错: {str(e)}'}), 500

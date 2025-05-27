import os
import uuid
import zipfile
from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
import io
import sys
import platform

from src.routes.pdf_to_image import pdf_to_image_bp

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

def check_poppler_installed():
    """检查poppler是否已安装并在PATH中"""
    system = platform.system()
    try:
        if system == 'Windows':
            # 检查Windows下是否有poppler的bin目录在PATH中
            paths = os.environ.get('PATH', '').split(';')
            for path in paths:
                if os.path.exists(path) and 'poppler' in path.lower() and os.path.exists(os.path.join(path, 'pdftoppm.exe')):
                    return True
            return False
        else:
            # 在Linux/Mac上检查pdftoppm命令是否可用
            import subprocess
            subprocess.run(['pdftoppm', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
    except (FileNotFoundError, subprocess.SubprocessError):
        return False

def convert_pdf_to_images_alternative(pdf_path, output_dir, format_type='jpg', dpi=200):
    """使用PyMuPDF作为替代方案转换PDF到图片"""
    try:
        import fitz  # PyMuPDF
        
        doc = fitz.open(pdf_path)
        image_paths = []
        
        for i in range(len(doc)):
            page = doc.load_page(i)
            pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
            
            img_filename = f"page_{i+1}.{format_type}"
            img_path = os.path.join(output_dir, img_filename)
            
            pix.save(img_path)
            image_paths.append(img_path)
        
        doc.close()
        return image_paths, len(doc)
    except ImportError:
        raise ImportError("无法导入PyMuPDF (fitz)。请安装: pip install PyMuPDF")

@pdf_to_image_bp.route('/convert', methods=['POST'])
def convert_pdf_to_image():
    """
    将PDF文件转换为图片
    
    请求参数:
    - file: PDF文件
    - format: 图片格式 (jpg, png, 默认为jpg)
    - dpi: 图片DPI (默认为200)
    
    返回:
    - 成功: {"success": true, "download_url": "下载链接", "page_count": 页数}
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
    
    # 获取参数
    format_type = request.form.get('format', 'jpg').lower()
    if format_type not in ['jpg', 'png']:
        format_type = 'jpg'
    
    try:
        dpi = int(request.form.get('dpi', 200))
    except ValueError:
        dpi = 200
    
    try:
        # 生成安全的文件名并保存上传的文件
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())
        pdf_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_{filename}")
        file.save(pdf_path)
        
        # 创建一个目录来存储图片
        images_dir = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}_images")
        os.makedirs(images_dir, exist_ok=True)
        
        # 尝试使用pdf2image转换
        try:
            from pdf2image import convert_from_path
            
            # 检查poppler是否已安装
            if not check_poppler_installed():
                raise ImportError("Poppler未安装或不在PATH中")
            
            # 执行PDF到图片的转换
            images = convert_from_path(pdf_path, dpi=dpi)
            
            # 保存图片
            image_paths = []
            for i, image in enumerate(images):
                img_filename = f"page_{i+1}.{format_type}"
                img_path = os.path.join(images_dir, img_filename)
                if format_type == 'jpg':
                    image.save(img_path, 'JPEG')
                else:
                    image.save(img_path, 'PNG')
                image_paths.append(img_path)
            
            page_count = len(images)
            
        except (ImportError, Exception) as e:
            # 如果pdf2image失败，尝试使用PyMuPDF作为替代方案
            image_paths, page_count = convert_pdf_to_images_alternative(pdf_path, images_dir, format_type, dpi)
        
        # 创建ZIP文件
        zip_filename = f"{os.path.splitext(filename)[0]}_images.zip"
        zip_path = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}_{zip_filename}")
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for img_path in image_paths:
                zipf.write(img_path, os.path.basename(img_path))
        
        # 生成下载URL
        download_url = f"/static/downloads/{unique_id}_{zip_filename}"
        
        # 删除上传的PDF文件和临时图片（可选）
        # os.remove(pdf_path)
        # for img_path in image_paths:
        #     os.remove(img_path)
        # os.rmdir(images_dir)
        
        return jsonify({
            'success': True, 
            'download_url': download_url,
            'filename': zip_filename,
            'page_count': page_count
        })
        
    except Exception as e:
        error_message = str(e)
        if "poppler" in error_message.lower():
            error_message = "PDF转图片需要安装Poppler。请访问 https://github.com/oschwartz10612/poppler-windows/releases 下载并安装，然后将bin目录添加到系统PATH环境变量中。"
        
        return jsonify({'success': False, 'error': f'转换过程中出错: {error_message}'}), 500

import os
import uuid
from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
from PIL import Image
import io
import imghdr

from src.routes.image_resize import image_resize_bp

# 配置上传和下载路径
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'uploads')
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'downloads')

# 确保目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_image_format(file_path):
    """获取图片的实际格式"""
    try:
        with Image.open(file_path) as img:
            return img.format.lower() if img.format else None
    except Exception:
        return None

@image_resize_bp.route('/resize', methods=['POST'])
def resize_image():
    """
    调整图片分辨率
    
    请求参数:
    - file: 图片文件
    - width: 新宽度 (像素)
    - height: 新高度 (像素)
    - keep_ratio: 是否保持宽高比 (true/false，默认为true)
    - format: 输出图片格式 (jpg, png, 默认为auto，自动匹配输入格式)
    
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
        return jsonify({'success': False, 'error': '不支持的文件类型，仅支持图片文件 (png, jpg, jpeg, gif, bmp, webp)'}), 400
    
    # 获取参数
    try:
        width = int(request.form.get('width', 0))
        height = int(request.form.get('height', 0))
    except ValueError:
        return jsonify({'success': False, 'error': '宽度和高度必须是整数'}), 400
    
    if width <= 0 and height <= 0:
        return jsonify({'success': False, 'error': '至少需要指定宽度或高度'}), 400
    
    keep_ratio = request.form.get('keep_ratio', 'true').lower() == 'true'
    
    format_type = request.form.get('format', 'auto').lower()
    if format_type not in ['jpg', 'png', 'auto']:
        format_type = 'auto'
    
    try:
        # 生成安全的文件名并保存上传的文件
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())
        img_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_{filename}")
        file.save(img_path)
        
        # 检测原始图片格式
        original_format = get_image_format(img_path)
        if not original_format:
            original_format = os.path.splitext(filename)[1][1:].lower()
            if original_format == 'jpeg':
                original_format = 'jpg'
        
        # 如果格式为auto，则使用原始图片格式
        if format_type == 'auto':
            if original_format in ['jpg', 'jpeg']:
                format_type = 'jpg'
            elif original_format == 'png':
                format_type = 'png'
            else:
                # 对于其他格式，默认使用jpg
                format_type = 'jpg'
        
        # 打开图片
        img = Image.open(img_path)
        
        # 计算新尺寸
        original_width, original_height = img.size
        new_width, new_height = width, height
        
        if keep_ratio:
            if width > 0 and height > 0:
                # 如果同时指定了宽度和高度，并且保持比例，则使用较小的缩放比例
                ratio_width = width / original_width
                ratio_height = height / original_height
                ratio = min(ratio_width, ratio_height)
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
            elif width > 0:
                # 只指定了宽度
                ratio = width / original_width
                new_height = int(original_height * ratio)
            elif height > 0:
                # 只指定了高度
                ratio = height / original_height
                new_width = int(original_width * ratio)
        else:
            # 不保持比例，如果某个维度未指定，则使用原始尺寸
            if width <= 0:
                new_width = original_width
            if height <= 0:
                new_height = original_height
        
        # 调整图片大小
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # 保存结果
        output_filename = f"resized_{os.path.splitext(filename)[0]}.{format_type}"
        output_path = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}_{output_filename}")
        
        if format_type == 'jpg':
            resized_img.save(output_path, 'JPEG', quality=95)
        else:
            resized_img.save(output_path, 'PNG')
        
        # 生成下载URL
        download_url = f"/static/downloads/{unique_id}_{output_filename}"
        
        # 关闭图像
        img.close()
        resized_img.close()
        
        # 删除上传的图片（可选）
        # os.remove(img_path)
        
        return jsonify({
            'success': True, 
            'download_url': download_url,
            'filename': output_filename,
            'original_size': {
                'width': original_width,
                'height': original_height
            },
            'new_size': {
                'width': new_width,
                'height': new_height
            },
            'original_format': original_format,
            'output_format': format_type
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'调整分辨率过程中出错: {str(e)}'}), 500

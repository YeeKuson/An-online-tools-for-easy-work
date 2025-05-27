import os
import uuid
from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
from PIL import Image
import io

from src.routes.image_concat import image_concat_bp

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

@image_concat_bp.route('/concat', methods=['POST'])
def concat_images():
    """
    拼接多张图片
    
    请求参数:
    - files: 多个图片文件
    - direction: 拼接方向 (horizontal 或 vertical，默认为horizontal)
    - format: 输出图片格式 (jpg, png, 默认为jpg)
    
    返回:
    - 成功: {"success": true, "download_url": "下载链接"}
    - 失败: {"success": false, "error": "错误信息"}
    """
    # 检查是否有文件上传
    if 'files[]' not in request.files:
        return jsonify({'success': False, 'error': '没有上传文件'}), 400
    
    files = request.files.getlist('files[]')
    
    # 检查是否有文件
    if len(files) < 2:
        return jsonify({'success': False, 'error': '至少需要上传两张图片进行拼接'}), 400
    
    # 检查文件类型
    for file in files:
        if file.filename == '':
            return jsonify({'success': False, 'error': '存在未命名的文件'}), 400
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': f'不支持的文件类型: {file.filename}，仅支持图片文件 (png, jpg, jpeg, gif, bmp, webp)'}), 400
    
    # 获取参数
    direction = request.form.get('direction', 'horizontal').lower()
    if direction not in ['horizontal', 'vertical']:
        direction = 'horizontal'
    
    format_type = request.form.get('format', 'jpg').lower()
    if format_type not in ['jpg', 'png']:
        format_type = 'jpg'
    
    try:
        # 保存上传的图片并打开
        unique_id = str(uuid.uuid4())
        image_paths = []
        images = []
        
        for file in files:
            filename = secure_filename(file.filename)
            img_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_{filename}")
            file.save(img_path)
            image_paths.append(img_path)
            images.append(Image.open(img_path))
        
        # 计算拼接后的尺寸
        if direction == 'horizontal':
            total_width = sum(img.width for img in images)
            max_height = max(img.height for img in images)
            
            # 创建新图像
            result_img = Image.new('RGB', (total_width, max_height))
            
            # 拼接图像
            x_offset = 0
            for img in images:
                result_img.paste(img, (x_offset, 0))
                x_offset += img.width
        else:  # vertical
            max_width = max(img.width for img in images)
            total_height = sum(img.height for img in images)
            
            # 创建新图像
            result_img = Image.new('RGB', (max_width, total_height))
            
            # 拼接图像
            y_offset = 0
            for img in images:
                result_img.paste(img, (0, y_offset))
                y_offset += img.height
        
        # 保存结果
        output_filename = f"concat_image.{format_type}"
        output_path = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}_{output_filename}")
        
        if format_type == 'jpg':
            result_img.save(output_path, 'JPEG', quality=95)
        else:
            result_img.save(output_path, 'PNG')
        
        # 生成下载URL
        download_url = f"/static/downloads/{unique_id}_{output_filename}"
        
        # 关闭图像
        for img in images:
            img.close()
        
        # 删除上传的图片（可选）
        # for img_path in image_paths:
        #     os.remove(img_path)
        
        return jsonify({
            'success': True, 
            'download_url': download_url,
            'filename': output_filename
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'拼接过程中出错: {str(e)}'}), 500

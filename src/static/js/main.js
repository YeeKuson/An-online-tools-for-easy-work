// 全局JavaScript函数
document.addEventListener('DOMContentLoaded', function() {
    // 文件上传区域拖放功能
    const fileUploadAreas = document.querySelectorAll('.file-upload-area');
    
    if (fileUploadAreas) {
        fileUploadAreas.forEach(area => {
            area.addEventListener('dragover', function(e) {
                e.preventDefault();
                this.classList.add('dragover');
            });
            
            area.addEventListener('dragleave', function(e) {
                e.preventDefault();
                this.classList.remove('dragover');
            });
            
            area.addEventListener('drop', function(e) {
                e.preventDefault();
                this.classList.remove('dragover');
                
                const fileInput = this.querySelector('input[type="file"]');
                if (fileInput) {
                    fileInput.files = e.dataTransfer.files;
                    // 触发change事件
                    const event = new Event('change', { bubbles: true });
                    fileInput.dispatchEvent(event);
                }
            });
        });
    }
    
    // 文件大小格式化
    window.formatFileSize = function(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };
    
    // 显示错误消息
    window.showError = function(message) {
        const errorElement = document.querySelector('.error-message');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
            
            // 5秒后自动隐藏
            setTimeout(() => {
                errorElement.style.display = 'none';
            }, 5000);
        }
    };
    
    // 显示成功消息
    window.showSuccess = function(message) {
        const successElement = document.querySelector('.success-message');
        if (successElement) {
            successElement.textContent = message;
            successElement.style.display = 'block';
            
            // 5秒后自动隐藏
            setTimeout(() => {
                successElement.style.display = 'none';
            }, 5000);
        }
    };
    
    // 显示加载动画
    window.showLoading = function() {
        const loadingElement = document.querySelector('.loading-spinner');
        if (loadingElement) {
            loadingElement.style.display = 'block';
        }
    };
    
    // 隐藏加载动画
    window.hideLoading = function() {
        const loadingElement = document.querySelector('.loading-spinner');
        if (loadingElement) {
            loadingElement.style.display = 'none';
        }
    };
    
    // 显示结果容器
    window.showResult = function() {
        const resultElement = document.querySelector('.result-container');
        if (resultElement) {
            resultElement.style.display = 'block';
        }
    };
    
    // 隐藏结果容器
    window.hideResult = function() {
        const resultElement = document.querySelector('.result-container');
        if (resultElement) {
            resultElement.style.display = 'none';
        }
    };
});

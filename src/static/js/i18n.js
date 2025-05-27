// 多语言支持
const translations = {
    'zh': {
        'site_name': 'Nuno工具小站',
        'site_description': '一站式文件转换与图片处理工具',
        'pdf_to_word': 'PDF转Word',
        'pdf_to_word_desc': '将PDF文档转换为可编辑的Word文件，保留原始格式和布局。',
        'word_to_pdf': 'Word转PDF',
        'word_to_pdf_desc': '将Word文档转换为PDF格式，适合分享和打印。',
        'pdf_to_image': 'PDF转图片',
        'pdf_to_image_desc': '将PDF文档的每一页转换为高质量图片。',
        'pdf_to_ppt': 'PDF转PPT',
        'pdf_to_ppt_desc': '将PDF文档转换为PowerPoint演示文稿，方便演示和编辑。',
        'image_concat': '图片拼接',
        'image_concat_desc': '将多张图片水平或垂直拼接成一张完整图片。',
        'image_resize': '图片调整分辨率',
        'image_resize_desc': '调整图片尺寸和分辨率，满足不同场景需求。',
        'more_tools': '更多工具',
        'more_tools_desc': '更多实用工具即将推出，敬请期待...',
        'coming_soon': '即将推出',
        'use_tool': '使用工具',
        'upload_file': '上传文件',
        'drag_drop': '拖放文件到这里或点击上传',
        'convert': '转换',
        'download': '下载',
        'processing': '处理中...',
        'success': '成功！',
        'error': '错误：',
        'back_to_home': '返回首页',
        'page_not_found': '页面未找到',
        'page_not_found_desc': '您访问的页面不存在或已被移除。',
        'footer_copyright': '© 2025 Nuno工具小站. 保留所有权利。',
        'github_repo': 'GitHub代码仓库',
        'language': '语言',
        'chinese': '中文',
        'english': '英文'
    },
    'en': {
        'site_name': 'Nuno Tools Station',
        'site_description': 'One-stop File Conversion and Image Processing Tools',
        'pdf_to_word': 'PDF to Word',
        'pdf_to_word_desc': 'Convert PDF documents to editable Word files, preserving original format and layout.',
        'word_to_pdf': 'Word to PDF',
        'word_to_pdf_desc': 'Convert Word documents to PDF format, ideal for sharing and printing.',
        'pdf_to_image': 'PDF to Image',
        'pdf_to_image_desc': 'Convert each page of PDF documents to high-quality images.',
        'pdf_to_ppt': 'PDF to PPT',
        'pdf_to_ppt_desc': 'Convert PDF documents to PowerPoint presentations for easy presentation and editing.',
        'image_concat': 'Image Concatenation',
        'image_concat_desc': 'Concatenate multiple images horizontally or vertically into one complete image.',
        'image_resize': 'Image Resolution Adjustment',
        'image_resize_desc': 'Adjust image size and resolution to meet different scenario requirements.',
        'more_tools': 'More Tools',
        'more_tools_desc': 'More useful tools coming soon, stay tuned...',
        'coming_soon': 'Coming Soon',
        'use_tool': 'Use Tool',
        'upload_file': 'Upload File',
        'drag_drop': 'Drag and drop files here or click to upload',
        'convert': 'Convert',
        'download': 'Download',
        'processing': 'Processing...',
        'success': 'Success!',
        'error': 'Error: ',
        'back_to_home': 'Back to Home',
        'page_not_found': 'Page Not Found',
        'page_not_found_desc': 'The page you are looking for does not exist or has been removed.',
        'footer_copyright': '© 2025 Nuno Tools Station. All rights reserved.',
        'github_repo': 'GitHub Repository',
        'language': 'Language',
        'chinese': 'Chinese',
        'english': 'English'
    }
};

// 当前语言
let currentLang = 'zh';

// 切换语言
function switchLanguage(lang) {
    currentLang = lang;
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[lang][key]) {
            element.textContent = translations[lang][key];
        }
    });
    
    // 更新语言按钮状态
    document.querySelectorAll('.lang-btn').forEach(btn => {
        if (btn.getAttribute('data-lang') === lang) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    // 保存语言偏好到本地存储
    localStorage.setItem('preferred_language', lang);
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', function() {
    // 检查本地存储中的语言偏好
    const savedLang = localStorage.getItem('preferred_language');
    if (savedLang && (savedLang === 'zh' || savedLang === 'en')) {
        currentLang = savedLang;
    }
    
    // 初始化语言
    switchLanguage(currentLang);
    
    // 添加语言切换按钮事件监听
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const lang = this.getAttribute('data-lang');
            switchLanguage(lang);
        });
    });
});

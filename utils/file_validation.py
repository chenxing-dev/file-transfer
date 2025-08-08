from flask import current_app
import re


def allowed_file_type(filename):
    """检查文件是否允许"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    print(f"Checking file type for extension: {ext}")
    for category, exts in current_app.config['ALLOWED_EXTENSIONS'].items():
        if ext in exts:
            print(f"文件类型 {ext} 在允许的列表中: {category}")
            return True
    print(f"文件类型 {ext} 不在允许的列表中")
    return False


def get_file_category(filename):
    """获取文件类型分类"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    for category, exts in current_app.config['ALLOWED_EXTENSIONS'].items():
        if ext in exts:
            return category
    return 'other'


def validate_file_size(file):
    """Validate file size based on file type"""
    filename = file.filename
    file_size = len(file.read())
    file.seek(0)  # Reset file pointer

    file_type = get_file_category(filename)

    # Get size limits from config
    max_sizes = {
        'image': current_app.config.get('MAX_IMAGE_SIZE', 10 * 1024 * 1024),
        'video': current_app.config.get('MAX_VIDEO_SIZE', 50 * 1024 * 1024),
        'document': current_app.config.get('MAX_DOCUMENT_SIZE', 5 * 1024 * 1024),
        'audio': current_app.config.get('MAX_AUDIO_SIZE', 20 * 1024 * 1024),
        'other': current_app.config.get('MAX_FILE_SIZE', 10 * 1024 * 1024)
    }

    max_size = max_sizes.get(file_type, max_sizes['other'])

    if file_size > max_size:
        return False, f"File too large. Max size for {file_type}s is {human_readable_size(max_size)}"

    return True, ""


def human_readable_size(size_bytes):
    """Convert bytes to human-readable format"""
    if size_bytes == 0:
        return "0B"
    units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = 0
    while size_bytes >= 1024 and i < len(units) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {units[i]}"

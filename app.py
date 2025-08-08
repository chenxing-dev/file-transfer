"""文件传输应用"""

# pylint:disable=
from datetime import datetime
import os
import socket
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename

from utils.file_validation import allowed_file_type, get_all_allowed_extensions, get_file_category, validate_file_size, get_file_type_mapping

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"  # 保存文件的目录
DOWNLOAD_FOLDER = 'downloads'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
PORT = 8080  # 开发端口

# File size configuration (in bytes)
app.config.update({
    'MAX_CONTENT_LENGTH': 100 * 1024 * 1024,  # 100MB total request size
    'MAX_FILE_SIZE': 50 * 1024 * 1024,        # 50MB per file
    'MAX_IMAGE_SIZE': 10 * 1024 * 1024,        # 10MB for images
    'MAX_VIDEO_SIZE': 50 * 1024 * 1024,        # 50MB for videos
    'MAX_DOCUMENT_SIZE': 5 * 1024 * 1024,      # 5MB for documents
    'ALLOWED_FILE_TYPE': {
        'image': {
            'name': '图片',
            'extensions': ['png', 'jpg', 'jpeg', 'gif', 'webp'],
            'icon': 'fas fa-image',
            'style': 'bg-green-100 text-green-600'
        },
        'audio': {
            'name': '音频',
            'extensions': ['m4a', 'mp3', 'wav', 'flac',],
            'icon': 'fas fa-file-audio',
            'style': 'bg-purple-100 text-purple-600'
        },
        'pdf': {
            'name': '文档',
            'extensions': ['pdf'],
            'icon': 'fas fa-file-pdf',
            'style': 'bg-red-100 text-red-600'
        },
        'text': {
            'name': '文档',
            'extensions': ['txt'],
            'icon': 'fas fa-file-alt',
            'style': 'bg-indigo-100 text-indigo-600'
        },
        'word': {
            'name': '文档',
            'extensions': ['doc', 'docx'],
            'icon': 'fas fa-file-word',
            'style': 'bg-blue-100 text-blue-600'
        },
        'excel': {
            'name': '文档',
            'extensions': ['xls', 'xlsx'],
            'icon': 'fas fa-file-excel',
            'style': 'bg-green-100 text-green-600'
        },
        'powerpoint': {
            'name': '文档',
            'extensions': ['ppt', 'pptx'],
            'icon': 'fas fa-file-powerpoint',
            'style': 'bg-orange-100 text-orange-600'
        },
        'video': {
            'name': '视频',
            'extensions': ['mp4'],
            'icon': 'fas fa-file-video',
            'style': 'bg-pink-100 text-pink-600'
        },
        'archive': {
            'name': '压缩包',
            'extensions': ['zip', 'rar', '7z'],  
            'icon': 'fas fa-file-archive',
            'style': 'bg-yellow-100 text-yellow-600'
        }
    }
})


def get_local_ip():
    """获取本机IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return "0.0.0.0"


def prepare_directories():
    """准备上传和下载目录"""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


prepare_directories()


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """文件上传页面"""
    if request.method == 'POST':
        if 'file' not in request.files:
            return {"status": "error", "message": "没有文件部分"}, 400

        files = request.files.getlist('file')
        if len(files) == 0 or files[0].filename == '':
            return {"status": "error", "message": "未选择文件"}, 400

        results = []
        for file in files:
            # Skip empty files
            if file and file.filename != '':
                # Validate file size
                size_valid, size_error = validate_file_size(file)
                if size_valid:
                    # Validate file type
                    if allowed_file_type(filename=file.filename):
                        # 生成唯一文件名
                        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                        filename = f"{timestamp}_{secure_filename(file.filename)}"
                        save_path = os.path.join(
                            app.config['UPLOAD_FOLDER'], filename)
                        try:
                            file.save(save_path)
                            results.append({
                                "status": "success",
                                "filename": filename,
                                "size": os.path.getsize(save_path),
                                "type": get_file_category(file.filename)
                            })
                        except OSError as e:
                            results.append({
                                "status": "error",
                                "filename": file.filename,
                                "message": f"保存文件失败: {str(e)}"
                            })
                    else:
                        results.append({
                            "status": "error",
                            "filename": file.filename,
                            "message": "不支持的文件类型"
                        })
                else:
                    results.append({
                        'filename': file.filename,
                        'status': 'error',
                        'message': size_error
                    })
        print(f"上传结果: {results}")
        return {"results": results}

    # GET请求返回上传页面
    return render_template('upload.html', allowed_file_type=app.config['ALLOWED_FILE_TYPE'])


@app.route('/download')
def download():
    """文件下载页面"""
    # 获取downloads目录下的文件列表
    files = []
    for filename in os.listdir(app.config['DOWNLOAD_FOLDER']):
        path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
        if os.path.isfile(path):
            files.append({
                "name": filename,
                "size": os.path.getsize(path),
                "modified": datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M')
            })

    return render_template('download.html', files=files, file_type_mapping=get_file_type_mapping())


@app.route('/download-file/<filename>')
def download_file(filename):
    """下载指定文件"""
    path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    if not os.path.exists(path):
        return "文件不存在", 404

    # 防止路径遍历攻击
    if '../' in filename or not os.path.isfile(path):
        return "无效的文件请求", 400

    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    local_ip = get_local_ip()
    print(f"请访问: http://{local_ip}:{PORT}")
    print("功能说明:")
    print("1. 上传文件到电脑: /upload")
    print("2. 从电脑下载文件: /download")
    app.run(host='0.0.0.0', port=PORT, threaded=True)

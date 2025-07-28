"""文件传输应用"""

# pylint:disable=
from datetime import datetime
import os
import socket
from flask import Flask, request, render_template, send_file, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"  # 保存文件的目录
DOWNLOAD_FOLDER = 'downloads'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
PORT = 8080  # 开发端口

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {
    'image': ['png', 'jpg', 'jpeg', 'gif', 'webp'],
    'audio': ['m4a', 'mp3', 'wav', 'flac', 'ogg'],
    'document': ['pdf', 'txt', 'doc', 'docx', 'xlsx']
}


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

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    for category, exts in ALLOWED_EXTENSIONS.items():
        if ext in exts:
            return True
    return False

def get_file_category(filename):
    """获取文件类型分类"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    for category, exts in ALLOWED_EXTENSIONS.items():
        if ext in exts:
            return category
    return 'other'

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
            if file and allowed_file(file.filename):
                # 生成唯一文件名
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                filename = f"{timestamp}_{secure_filename(file.filename)}"
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
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
                allowed_exts = []
                for exts in ALLOWED_EXTENSIONS.values():
                    allowed_exts.extend(exts)
                results.append({
                    "status": "error",
                    "filename": file.filename,
                    "message": f"不支持的文件类型，支持格式: {', '.join(allowed_exts)}"
                })
        
        return {"results": results}
    
    # GET请求返回上传页面
    return render_template('upload.html', allowed_extensions=ALLOWED_EXTENSIONS)

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
    
    return render_template('download.html', files=files)

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

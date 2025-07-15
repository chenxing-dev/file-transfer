"""文件传输应用"""

# pylint:disable=C0116
from datetime import datetime
import os
import socket
from flask import Flask, request, render_template


app = Flask(__name__)
UPLOAD_FOLDER = "uploads"  # 保存文件的目录
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
PORT = 8080  # 开发端口


# 获取本机IP地址
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "0.0.0.0"


# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return {"status": "error", "message": "没有文件部分"}, 400

    files = request.files.getlist("file")
    if len(files) == 0 or files[0].filename == "":
        return {"status": "error", "message": "未选择文件"}, 400

    results = []
    for file in files:
        if file and file.filename.lower().endswith(".png"):
            # 生成唯一文件名
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            filename = f"{timestamp}_{file.filename}"
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)
            results.append(
                {
                    "status": "success",
                    "filename": filename,
                    "size": os.path.getsize(save_path),
                }
            )
        else:
            results.append(
                {
                    "status": "error",
                    "filename": file.filename,
                    "message": "仅支持PNG文件",
                }
            )

    return {"results": results}


if __name__ == "__main__":
    local_ip = get_local_ip()
    print(f"请访问: http://{local_ip}:{PORT}")
    app.run(host="0.0.0.0", port=PORT)

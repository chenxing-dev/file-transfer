# 文件传输应用

这个项目是一个简单的本地文件传输解决方案，允许你通过设备浏览器直接将PNG文件传输到你的电脑上，无需任何第三方服务或云存储。

![应用截图](800x400?text=iPad+File+Transfer+Screenshot)

## 功能特点

- 🌐 通过本地网络直接传输
- ⚡ 简单易用的界面
- 🔒 本地网络传输，数据不经过第三方

## 快速开始

### 前提条件
- Python 3.6+
- Pip 包管理器

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/chenxing-dev/file-transfer.git
cd file-transfer
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 启动服务器：
```bash
python app.py
```

### 使用方法

1. 确保设备和电脑在**同一Wi-Fi网络**下
2. 在浏览器中访问：
```
http://<你的电脑IP>:8080
```
例如：
```
http://192.168.1.10:8080
```

1. 选择要传输的PNG文件并点击上传
2. 文件将保存在电脑的`uploads/`目录中

### 查找电脑IP地址
- **Windows**: 命令提示符输入 `ipconfig`
- **Mac/Linux**: 终端输入 `ip a`

## 项目结构

```
file-transfer/
├── templates/
│   └── upload.html       # 前端页面
├── uploads/              # 上传文件存储目录
├── app.py                # Flask主应用
├── README.md             # 项目文档
├── requirements.txt      # 依赖列表
└── TODO.md               # 项目待办事项
```

## 贡献指南

欢迎提交问题和拉取请求！请确保：
1. 在提交PR前运行代码检查
2. 保持代码风格一致
3. 为新增功能添加测试

## 许可证

本项目采用 [MIT 许可证](LICENSE)


# File Transfer Web Application

![File Transfer Demo](demo.gif)

A web application for file transfers between devices on the same network. Built with Flask and Tailwind CSS. 

这个项目是一个简单的本地文件传输解决方案，无需任何第三方服务或云存储。

## Features

- **Bidirectional file transfer**: Upload from any device to server, download from server to any device
- **Responsive design**: Works on mobile, tablet, and desktop
- **Security features**:
  - File type whitelisting
  - Secure filename handling
  - Unique filenames to prevent conflicts
- **Modern UI**:
  - Toast notifications
  - File type icons
  - Drag-and-drop uploads
  - Animated interactions
- **Search functionality**: Quickly find files by name

## Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Build Tools**: Tailwind CLI
- **Icons**: Font Awesome

## Installation

### Prerequisites
- Python 3.7+
- Node.js & npm (for Tailwind CSS)

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/chenxing-dev/file-transfer.git
cd file-transfer
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Install Tailwind CSS:
```bash
npm install -D tailwindcss @tailwindcss/cli
```

4. (Optional) Start the Tailwind CLI build process:
```bash
npx @tailwindcss/cli -i ./templates/src/input.css -o ./static/output.css --watch
```

5. Start the application:
```bash
python app.py
```

6. Access the application at: `http://127.0.0.1:8080`

## Usage

### Uploading Files
1. Click "开始上传" on the main page
2. Drag and drop files into the upload area or click to select files
3. Supported file types: images, documents, audio

### Downloading Files
1. Click "浏览文件" on the main page
2. Search for files using the search bar
3. Click the download button next to any file

## Project Structure

```
file-transfer/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── static/                # Static assets
│   ├── output.css         # Compiled Tailwind CSS
│   └── favicon.svg        # Application favicon
├── templates/             # HTML templates
│   ├── index.html         # Main page
│   ├── download.html      # Download page
│   ├── upload.html        # Upload page
│   └── src/               # Tailwind source files
│       └── input.css      # Tailwind input CSS
├── downloads/             # Files for the download page
├── uploads/               # Uploaded files storage
├── README.md              # Project documentation
└── TODO.md                # Development roadmap
```

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file 

# My Photo Editor

一个基于 Python Tkinter 和 Pillow 的简单照片编辑器，支持打开图片、调整亮度/对比度/饱和度、裁剪、撤销、重置和另存为。

## 项目结构

```text
my-photo-editor/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 安装与运行

建议使用虚拟环境安装依赖：

```bash
python -m venv venv
```

Windows：

```bash
venv\Scripts\activate
```

macOS/Linux：

```bash
source venv/bin/activate
```

安装 Pillow 并运行程序：

```bash
pip install -r requirements.txt
python main.py
```

## 依赖

- Pillow：读取、预览、调整和保存图片。
- Tkinter：Python 标准库中的图形界面组件，不需要单独写入 `requirements.txt`。

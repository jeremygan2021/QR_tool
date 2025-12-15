# 美化二维码生成器

这是一个能够生成各种美化二维码的Python工具。

## 功能特点

- 圆角二维码：生成带有圆角方块的二维码
- 圆形二维码：生成带有圆形点的二维码
- 渐变色二维码：生成具有渐变颜色效果的二维码
- 添加Logo：可以在二维码中央添加自定义Logo

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 网页版 (Docker)

1. 确保已安装 Docker 和 Docker Compose。
2. 在项目根目录下运行：

```bash
docker-compose up -d
```

3. 浏览器访问 `http://localhost:8711`。
4. 输入 URL，选择样式和尺寸，点击生成即可。

### 命令行版

```python
python qr_generator.py
```

这将使用默认设置生成三种二维码样式。

### 自定义用法 (Python脚本)

```python
from qr_generator import generate_styled_qr_code, generate_gradient_qr

# 生成圆角二维码
generate_styled_qr_code(
    "https://example.com",
    output_file="rounded_qr.png",
    color="#1E88E5",  # 蓝色
    style="rounded"
)

# 生成圆形点二维码
generate_styled_qr_code(
    "https://example.com",
    output_file="circle_qr.png",
    color="#8BC34A",  # 绿色
    style="circle"
)

# 生成带Logo的二维码
generate_styled_qr_code(
    "https://example.com",
    output_file="logo_qr.png",
    logo_path="your_logo.png",  # 替换为你的Logo图片路径
    color="#FF5722",  # 橙色
    style="rounded"
)

# 生成渐变色二维码
generate_gradient_qr(
    "https://example.com",
    output_file="gradient_qr.png",
    start_color="#FF5722",  # 橙色
    end_color="#9C27B0"  # 紫色
)
```

## 参数说明

### generate_styled_qr_code 函数参数

- `data`：要编码的数据（如URL、文本等）
- `output_file`：输出文件名
- `logo_path`：可选的Logo图片路径
- `color`：二维码颜色（十六进制）
- `bg_color`：背景颜色（十六进制）
- `box_size`：二维码方块大小
- `border`：边界大小
- `style`：样式（"rounded", "circle", "classic"）

### generate_gradient_qr 函数参数

- `data`：要编码的数据（如URL、文本等）
- `output_file`：输出文件名
- `start_color`：渐变起始颜色（十六进制）
- `end_color`：渐变结束颜色（十六进制）
- `bg_color`：背景颜色（十六进制）
- `box_size`：二维码方块大小
- `border`：边界大小
